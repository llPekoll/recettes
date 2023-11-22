from common.models import Rate, Tag
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from recipe.forms import RecipeForm
from recipe.models import Ingredient, Recipe, RecipeIngredient


def page_recipe_creation(request):
    form = RecipeForm()
    ingredient_names = [ingredient.name for ingredient in Ingredient.objects.all()]
    recipe_draft = Recipe.objects.filter(author=request.user, is_draft=True).last()
    ings = [
        ingredient
        for ingredient in RecipeIngredient.objects.filter(recipe=recipe_draft)
    ]
    tags = Tag.objects.all()
    return render(
        request,
        "new_recipe.html",
        {
            "form": form,
            "ingredient_names": ingredient_names,
            "ings": ings,
            "create": True,
            "tag_list": [tag.name for tag in tags],
        },
    )


def page_recipe_detail(request, pk):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=pk)
    is_author = recipe.author == user
    is_favorite = recipe in user.favorite_recipes.all()
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    comments = recipe.comments.order_by("-created_at")
    try:
        rate = Rate.objects.get(user=request.user, recipe=recipe).value
        rate_average = Rate.objects.filter(recipe=recipe).aggregate(Avg("value"))[
            "value__avg"
        ]

    except Rate.DoesNotExist:
        rate = 3
        rate_average = 3
    number_of_rate_given = Rate.objects.filter(recipe=recipe).count()
    return render(
        request,
        "detail_recipe.html",
        {
            "recipe": recipe,
            "is_author": is_author,
            "is_favorite": is_favorite,
            "rate": rate,
            "ingredients": ingredients,
            "comments": comments,
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
        "new_recipe.html",
        {
            "form": form,
            "ings": ings,
            "recipe": recipe,
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