from django.shortcuts import redirect, render

from .forms import RecipeForm, RecipeIngredientForm


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
    else:
        form = RecipeForm()
    return render(request, "new_recipe.html", {"form": form})


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
        return "jose"
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
