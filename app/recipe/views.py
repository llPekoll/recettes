from datetime import datetime

from account.models import User
from django.db.models import Avg, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from recipe.models import Recipe

from .forms import RecipeForm, RecipeIngredientForm
from .models import Comment, Ingredient, Rate, Recipe, RecipeIngredient, Tag


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
            "create": True,
        },
    )


def add_ingredient(request):
    if request.htmx:
        print(request.POST)
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

    comments = recipe.comments.order_by("-created_at")
    try:
        rate = Rate.objects.get(user=request.user, recipe=recipe).value
        rate_average = Rate.objects.filter(recipe=recipe).aggregate(Avg("value"))[
            "value__avg"
        ]

    except Rate.DoesNotExist:
        rate = 3
        rate_average = 3
    number_of_rate_given = Rate.objects.filter(recipe=recipe).count()
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

    return render(request, "star_rate.html", {"rate": obj.value})


def add_new_comment(request, pk):
    if request.htmx:
        recipe = get_object_or_404(Recipe, pk=pk)
        Comment.objects.create(
            author=request.user, content_object=recipe, text=request.POST.get("comment")
        )
    comments = recipe.comments.order_by("-created_at")
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


def add_tags(tags_in_string_format):
    tag_names = tags_in_string_format.split(",")


def add_recipe_tags(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        tag_names = request.POST.get("tags", "").split(",")
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                recipe.tags.add(tag)
                # better send the new content edited
        return HttpResponse("Content edited", status=200)
    # better send the new content edited
    return HttpResponse("Just didn't worked", status=400)


def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipe_detail", recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(
        request, "new_recipe.html", {"form": form, "recipe": recipe, "create": False}
    )
