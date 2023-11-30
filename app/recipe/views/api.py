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


def ingredient_list(request):
    recipe = request.POST.get("recipe")
    if recipe and "/" in recipe:
        recipe = Recipe.objects.create(author=request.user)
    else:
        recipe = Recipe.objects.get(id=recipe, author=request.user)

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data["recipe"] = recipe.id
        form = RecipeIngredientForm(post_data)
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
            {"ings": ings, "recipe": ingredient.recipe},
        )


def step_list(request):
    step_id = request.POST.get("step_id")
    if "/" in step_id:
        recipe = RecipeStep.objects.create(author=request.user)
    else:
        recipe = RecipeStep.objects.get(id=step_id, author=request.user)

    if request.method == "POST":
        form = RecipeStepForm(request.POST)
        form.recipe_id = recipe.id
        if form.is_valid():
            form.save()
        steps = [step for step in RecipeStep.objects.filter(recipe=recipe.id)]
        return render(
            request,
            "components/step_list.html",
            {"steps": steps, "recipe": recipe},
        )


def step_detail(request, pk):
    if request.method == "DELETE":
        step = get_object_or_404(RecipeStep, pk=pk)
        step.delete()
        steps = [step for step in RecipeStep.objects.filter(recipe=recipe.id)]

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
            recipe=recipe,
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
