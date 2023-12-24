from common.forms import CommentForm
from common.models import Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, render
from recipe.forms import RecipeForm, RecipeStepForm
from recipe.models import Ingredient, Recipe, RecipeIngredient


@login_required
def page_recipe_creation(request):
    form = RecipeForm()
    ingredient_names = [ingredient.name for ingredient in Ingredient.objects.all()]
    nb = Recipe.objects.count()
    recipe = Recipe.objects.create(author=request.user, title=f"New Recipe {nb + 1}")
    tags = Tag.objects.all()
    return render(
        request,
        "patterns/pages/list_recipe/create_edit_recipe.html",
        {
            "form": form,
            "recipeStepForm": RecipeStepForm(),
            "create": True,
            "recipe": recipe,
            "ingredient_names": ingredient_names,
            "tag_list": [tag.name for tag in tags],
        },
    )


def page_recipe_detail(request, pk):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=pk)
    if user.is_authenticated:
        is_favorite = recipe in user.favorite_recipes.all()
        rate = recipe.rates.filter(user=request.user).first()
        if rate:
            rate = rate.value or 3
        else:
            rate = False
    else:
        is_favorite = False
        rate = False

    rate_average = recipe.rates.aggregate(Avg("value"))["value__avg"]

    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    comments = recipe.comments.order_by("-created_at")
    steps = recipe.steps.all()
    number_of_rate_given = recipe.rates.count()
    return render(
        request,
        "detail_recipe.html",
        {
            "recipe": recipe,
            "is_favorite": is_favorite,
            "comment_form": CommentForm(),
            "ingredients": ingredients,
            "steps": steps,
            "comments": comments,
            "rate": rate,
            "given_rate": {
                "rate_average": rate_average,
                "number_of_rate_given": number_of_rate_given,
            },
        },
    )


def page_edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ings = recipe.ingredients.all()

    form = RecipeForm(instance=recipe)
    tags = Tag.objects.all()
    return render(
        request,
        "patterns/pages/list_recipe/create_edit_recipe.html",
        {
            "form": form,
            "ings": ings,
            "recipe": recipe,
            "recipeStepForm": RecipeStepForm(),
            "create": False,
            "tag_list": [tag.name for tag in tags],
        },
    )


def page_recipes(request):
    recipes = Recipe.objects.filter(is_draft=False)
    print(recipes)
    return render(
        request,
        "recipes.html",
        {
            "recipes": recipes,
        },
    )


def page_search_recipes(request):
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
