from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from datetime import datetime
from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient, Ingredient
from account.models import User


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
    recipe = get_object_or_404(Recipe, pk=pk)
    is_author = recipe.author == request.user
    return render(
        request,
        "detail_recipe.html",
        {"recipe": recipe, "is_author": is_author},
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
