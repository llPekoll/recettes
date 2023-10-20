from datetime import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q, Avg
from account.models import User

from .forms import RecipeForm, RecipeIngredientForm
from .models import Ingredient, Recipe, RecipeIngredient, Rate, Comment


def go_to_new_recipe(request):
    date = f"{datetime.now()}"[:-10]
    Recipe.objects.create(
        author=request.user,
        is_draft=True,
        title=f"New draft {date}",
    )
    return redirect("recipe-creation")


def recipe_creation(request):
    if request.method == "POST":
        recipe = Recipe.objects.get(
            author=request.user, is_draft=True, id=request.POST.get("recipe_id")
        )
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save()
        return redirect(reverse("recipe-detail", args=[recipe.id]))

    form = RecipeForm()
    ingredient_names = [ingredient.name for ingredient in Ingredient.objects.all()]
    recipe_draft = Recipe.objects.filter(author=request.user, is_draft=True).last()
    ings = [
        ingredient
        for ingredient in RecipeIngredient.objects.filter(recipe=recipe_draft)
    ]
    return render(
        request,
        "new_recipe.html",
        {
            "form": form,
            "ingredient_names": ingredient_names,
            "recipe_draft": recipe_draft.id,
            "ings": ings,
        },
    )


def add_ingredient(request):
    if request.htmx:
        form = RecipeIngredientForm(request.POST)
        print(form.errors)
        if form.is_valid():
            res = form.save()
        print(request.POST.get("recipe_id"))
        ings = [
            ingredient
            for ingredient in RecipeIngredient.objects.filter(
                recipe=request.POST.get("recipe_id")
            )
        ]
        return render(
            request,
            "ingredient_list.html",
            {
                "ings": ings,
            },
        )


def delete_ingredient(request, pk):
    ingredient = get_object_or_404(RecipeIngredient, pk=pk)
    ingredient.delete()
    ings = [
        ingredient
        for ingredient in RecipeIngredient.objects.filter(recipe=ingredient.recipe)
    ]

    return render(
        request,
        "ingredient_list.html",
        {
            "ings": ings,
        },
    )


def recipe_detail(request, pk):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=pk)
    is_author = recipe.author == user
    is_favorite = recipe in user.favorite_recipes.all()
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    comments = Comment.objects.filter(recipe=recipe).order_by("-created_at")
    print(comments[0].created_at)
    try:
        rate = Rate.objects.get(user=request.user, recipe=recipe).value
        rate_average = Rate.objects.filter(recipe=recipe).aggregate(Avg("value"))[
            "value__avg"
        ]
        number_of_rate_given = Rate.objects.filter(recipe=recipe).count()

    except Rate.DoesNotExist:
        rate = 3
    return render(
        request,
        "detail_recipe.html",
        {
            "recipe": recipe,
            "is_author": is_author,
            "is_favorite": is_favorite,
            "rate": rate,
            "ingredients": ingredients,
            "comments": comments,
            "given_rate": {
                "rate_average": rate_average,
                "number_of_rate_given": number_of_rate_given,
            },
        },
    )


def recipes(request):
    return render(
        request,
        "recipes.html",
        {
            "recipes": Recipe.objects.filter(is_draft=True, is_private=False),
        },
    )


def authors(request):
    return render(
        request,
        "authors.html",
        {
            "authors": User.objects.all(),
        },
    )


def recipe_favorite(request, pk):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe in user.favorite_recipes.all():
        print("remove")
        user.favorite_recipes.remove(recipe)
        is_favorite = False
    else:
        user.favorite_recipes.add(recipe)
        is_favorite = True
        print("add")
    return render(
        request,
        "is_favorite.html",
        {"recipe": recipe, "is_favorite": is_favorite},
    )


def recipe_rating(request, pk):
    if request.htmx:
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, _ = Rate.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={"value": request.POST.get("rate")},
        )

    return render(request, "rate.html", {"rate": obj.value})


def add_new_comment(request, pk):
    if request.htmx:
        recipe = get_object_or_404(Recipe, pk=pk)
        Comment.objects.create(
            recipe=recipe,
            author=request.user,
            text=request.POST.get("comment"),
        )
    comments = Comment.objects.filter(recipe=recipe).order_by("-created_at")
    return render(request, "rate.html", {"comment": comments})


def search_recipes(request):
    print(request.POST)
    if request.htmx:
        # include
        search_query = request.POST.get("search")
        recipes = Recipe.objects.filter(
            # Q(title__unaccent__icontains=search_query)
            # | Q(description__search=search_query)
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
        )
        return render(request, "recipe_list.html", {"recipes": recipes})


# def edit_comment(request, pk):
