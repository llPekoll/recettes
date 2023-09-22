from django.shortcuts import redirect, render
from datetime import datetime
from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient


def got_to_new_recipe(request):
    date = f"{datetime.now()}"[:-10]
    Recipe.objects.create(
        author=request.user,
        is_draft=True,
        title=f"New draft {date}",
    )
    return redirect("new-recipe")


def new_recipe(request):
    if request.method == "POST":
        print(request.POST)
        print("ok")
        form = RecipeForm(request.POST, instance=request.user)
        print(form.is_valid)
        print(form.errors)
        if form.is_valid():
            print("test passed")
            recipe = form.save(commit=False)
            # make slug
            recipe.save()
            print(recipe.id)
            return redirect("recipe:detail", recipe_id=recipe.id)

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
    print("willamse")
    if request.htmx:
        print("sako")
        print(request.POST)
        ingredient = request.POST.get("ingredient")
        print("form")
        print("for2")
        form = RecipeIngredientForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.base_fields)
            res = form.save()
            print(res.pk)
            print(res.ingredient)
        ings = [
            ingredient
            for ingredient in RecipeIngredient.objects.filter(
                recipe=request.POST.get("recipe")
            )
        ]
        return render(
            request,
            "ingredient_list.html",
            {
                "ings": ings,
            },
        )
    return "jose"


def delete_ingredient(request, pk):
    return "jose"


# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Ingredient, Recipe

# from .serializers import RecipeSerializer, IngredientSerializer


# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


# class IngredientViewSet(viewsets.ModelViewSet):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
