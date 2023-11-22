import json

from common.models import Image, Rate, Tag
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from recipe.forms import RecipeForm, RecipeIngredientForm
from recipe.models import Recipe, RecipeIngredient


def recipe_edit(request, pk):
    if request.method == "POST":
        recipe = get_object_or_404(Recipe, pk=pk)
        form = RecipeForm(request.POST, instance=recipe)
        id = recipe_write(form, request)
        return redirect(reverse("recipe:detail", args=[id]))
    return HttpResponse("Method not allowed", status=405)


def recipe_creation(request):
    if request.method == "POST":
        recipe = Recipe.objects.filter(pk=request.POST.get("recipe_id")).first()
        if recipe:
            form = RecipeForm(request.POST, instance=recipe)
        else:
            form = RecipeForm(request.POST)
        id = recipe_write(form, request)
        return redirect(reverse("recipe:detail", args=[id]))
    return HttpResponse("Method not allowed", status=405)


def recipe_write(form, request):
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        if request.POST.get("tags"):
            tags = json.loads(request.POST.get("tags"))
            for tag in tags:
                tag, _ = Tag.objects.get_or_create(name=tag.get("value"))
                recipe.tags.add(tag)
        if "image" in request.FILES:
            print(request.FILES["image"])
            image = Image(image=request.FILES["image"])
            image.save()
            recipe.image = image
        recipe.save()
        return recipe.id
    else:
        # TODO:
        # tell user something went wrong
        print(form.errors)
        return HttpResponse("the form is not valid", status=410)


# hugues brimel njinkoue
def ingredient_list(request):
    recipe_id = request.POST.get("recipe_id")
    if "/" in recipe_id:
        recipe = Recipe.objects.create(author=request.user)
    else:
        recipe = Recipe.objects.get(id=recipe_id, author=request.user)

    if request.method == "POST":
        form = RecipeIngredientForm(request.POST)
        form.recipe_id = recipe.id
        if form.is_valid():
            form.save()
            print("form.saved")
        ings = [
            ingredient
            for ingredient in RecipeIngredient.objects.filter(recipe=recipe.id)
        ]
        return render(
            request,
            "components/ingredient_list.html",
            {"ings": ings, "recipe": recipe},
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
