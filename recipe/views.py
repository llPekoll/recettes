from django.shortcuts import redirect, render

from .forms import RecipeForm
from .models import Recipe


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
