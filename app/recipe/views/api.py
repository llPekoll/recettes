import json

from common.models import Image, Rate, Tag
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from recipe.forms import RecipeForm, RecipeIngredientForm
from recipe.models import Recipe, RecipeIngredient


def recipe_edit(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Recipe, pk=pk)
        form = RecipeForm(request.POST, instance=article)
        recipe_write(form, request)


def recipe_creation(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        recipe_write(form, request)


def recipe_write(form, request):
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        if "tags" in request.POST:
            tags = json.loads(request.POST.get("tags"))
            for tag in tags:
                tag, _ = Tag.objects.get_or_create(name=tag.get("value"))
                recipe.tags.add(tag)
        if "image" in request.FILES:
            image = Image(image=request.FILES["image"])
            image.save()
            recipe.image = image
        recipe.save()
        return redirect(reverse("recipe:detail", args=[recipe.id]))
    else:
        # TODO:
        # tell user something went wrong
        print(form.errors)


def ingredient_list(request):
    if request.htmx:
        if request.method == "POST":
            form = RecipeIngredientForm(request.POST)
            if form.is_valid():
                form.save()
            ings = [
                ingredient
                for ingredient in RecipeIngredient.objects.filter(
                    recipe=request.POST.get("recipe_id")
                )
            ]
            return render(
                request,
                "components/ingredient_list.html",
                {
                    "ings": ings,
                },
            )


def ingredient_detail(request, pk):
    if request.method == "DELETE":
        ingredient = get_object_or_404(RecipeIngredient, pk=pk)
        ingredient.delete()
        ings = [
            ingredient
            for ingredient in RecipeIngredient.objects.filter(recipe=ingredient.recipe)
        ]

        return render(
            request,
            "components/ingredient_list.html",
            {
                "ings": ings,
            },
        )


def set_favorite(request, pk):
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


def set_rating(request, pk):
    if request.htmx:
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, _ = Rate.objects.update_or_create(
            recipe=recipe,
            user=request.user,
            defaults={"value": request.POST.get("rate")},
        )

    return render(request, "star_rate.html", {"rate": obj.value})


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
