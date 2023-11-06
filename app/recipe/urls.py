from django.urls import path

from .views import (
    add_ingredient,
    add_new_comment,
    add_recipe_tags,
    authors,
    delete_ingredient,
    edit_recipe,
    go_to_new_recipe,
    recipe_creation,
    recipe_detail,
    recipe_favorite,
    recipe_rating,
    recipes,
    search_recipes,
)

urlpatterns = [
    path("new-recipe/", go_to_new_recipe, name="new-recipe"),
    path("recipe_creation/", recipe_creation, name="recipe-creation"),
    path("recipe/<int:pk>/", recipe_detail, name="recipe-detail"),
    path("recipe/<int:pk>/favorite", recipe_favorite, name="recipe-favorite"),
    path("recipe/<int:pk>/rating", recipe_rating, name="recipe-rating"),
    path("recipe/<int:pk>/comment/new", add_new_comment, name="recipe-comment-new"),
    path("recipe/<int:pk>/tags/", add_recipe_tags, name="add_recipe_tags"),
    path("recipe/<int:pk>/edit/", edit_recipe, name="edit_recipe"),
    path("recipes/search/", search_recipes, name="recipe-search"),
    path("recipes/", recipes, name="recipes"),
    path("authors/", authors, name="authors"),
    path("add-ingredient/", add_ingredient, name="add-ingredient"),
    path("delete-ingredient/<int:pk>/", delete_ingredient, name="delete-ingredient"),
    # path(
    #     "ingredients/<int:pk>/delete/",
    #     DeleteIngredientView.as_view(),
    #     name="delete_ingredient",
    # ),
    # path("recipes/", recipe_list, name="recipe-list"),
    # path("recipes/<int:pk>/", recipe_detail, name="recipe-detail"),
    # path("ingredients/", ingredient_list, name="ingredient-list"),
    # path("ingredients/<int:pk>/", ingredient_detail, name="ingredient-detail"),
    # path(
    #     "recipes/<int:pk>/add-ingredient/",
    #     AddIngredientView.as_view(),
    #     name="add_ingredient",
    # ),
]
