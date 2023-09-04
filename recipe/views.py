from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm


def new_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            return redirect("recipe:detail", recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, "new_recipe.html", {"form": form})
