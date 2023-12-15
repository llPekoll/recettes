import json

from common.models import Image, Rate, Tag
from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from recipe.forms import RecipeForm, RecipeIngredientForm, RecipeStepForm
from recipe.models import Recipe, RecipeIngredient, RecipeStep


def recipe_edit(request, pk):
    print(request.POST)
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=pk)
        form = RecipeForm(request.POST, instance=recipe)
        recipe_write(form, request)
        return redirect(reverse("recipe:detail", args=[pk]))
    if request.method == "DELETE":
        recipe = Recipe.objects.get(pk=pk)
        # recipe.delete()
        return redirect(reverse("profile"))
    return HttpResponse("Method not allowed", status=405)


# def recipe_creation(request):
#     if request.method == "POST":
#         recipe = Recipe.objects.get(pk=request.POST.get("recipe"))
#         form = RecipeForm(request.POST, instance=recipe)
#         id = recipe_write(form, request)
#         return redirect(reverse("recipe:detail", args=[id]))
#     return HttpResponse("Method not allowed", status=405)


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
        else:
            if not recipe.image:
                image = Image.objects.get(pk=15)
                recipe.image = image
        recipe.save()
        return recipe.id
    else:
        # TODO:
        # tell user something went wrong
        print(form.errors)
        return HttpResponse("the form is not valid", status=410)


def ingredient_list(request):
    recipe = Recipe.objects.get(id=request.POST.get("recipe"))
    if request.method == "POST":
        form = RecipeIngredientForm(request.POST)
        form.recipe_id = recipe.id
        if form.is_valid():
            form.save()
            print("form.saved")
        else:
            print(form.errors)
        ingredients = [
            ingredient
            for ingredient in RecipeIngredient.objects.filter(recipe=recipe.id)
        ]
        return render(
            request,
            "patterns/components/ingredient_list/ingredient_list.html",
            {"ingredients": ingredients, "recipe": recipe},
        )


def ingredient_detail(request, pk):
    print(1)
    if request.method == "DELETE":
        print(2)
        ingredient = get_object_or_404(RecipeIngredient, pk=pk)
        ingredient.delete()
        ings = [
            ingredient
            for ingredient in RecipeIngredient.objects.filter(recipe=ingredient.recipe)
        ]
        print(ings)

        return render(
            request,
            "patterns/components/ingredient_list/ingredient_list.html",
            {"ings": ings, "recipe": ingredient.recipe},
        )


def step_list(request):
    print(request.POST)
    recipe = Recipe.objects.get(id=request.POST.get("recipe"))
    if request.method == "POST":
        form = RecipeStepForm(request.POST)
        print(form.errors)
        if form.is_valid():
            step = form.save(commit=False)
            if "image" in request.FILES:
                image = Image(image=request.FILES["image"])
                image.save()
                print("image saved")
                step.image = image

            step.recipe = recipe
            step.save()
        steps = [step for step in RecipeStep.objects.filter(recipe=recipe)]
        return render(
            request,
            "patterns/components/step_list/step_list.html",
            {"steps": steps, "recipe": recipe},
        )


def step_detail(request, pk):
    if request.method == "DELETE":
        step = get_object_or_404(RecipeStep, pk=pk)
        step.delete()
        steps = [step for step in RecipeStep.objects.filter(recipe=step.recipe)]

        return render(
            request,
            "components/step_list.html",
            {
                "steps": steps,
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
            content_object=recipe,
            user=request.user,
            defaults={"value": request.POST.get("rate")},
        )

    return render(request, "star_rate.html", {"rate": obj.value})


def search_recipes(request):
    if request.htmx:
        search_query = request.POST.get("search")
        vector = SearchVector("title", "description", "instructions")
        query = SearchQuery(search_query)
        search_headline = SearchHeadline("title", query)
        recipes = (
            Recipe.objects.annotate(
                rank=SearchRank(vector, query),
                similarity=TrigramSimilarity("title", search_query),
            )
            .annotate(headline=search_headline)
            .filter(rank__gte=0.00001)
            .order_by("-rank")
        )
        return render(request, "recipe_list.html", {"recipes": recipes})
