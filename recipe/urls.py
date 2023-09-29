from django.urls import path

from .views import (
    add_ingredient,
    recipe_creation,
    go_to_new_recipe,
    delete_ingredient,
    recipe_detail,
    recipes,
    authors,
)

urlpatterns = [
    path("new-recipe/", go_to_new_recipe, name="new-recipe"),
    path("recipe_creation/", recipe_creation, name="recipe-creation"),
    path("add-ingredient/", add_ingredient, name="add-ingredient"),
    path("delete-ingredient/<int:pk>/", delete_ingredient, name="delete-ingredient"),
    path("recipe/<int:pk>/", recipe_detail, name="recipe-detail"),
    path("recipes/", recipes, name="recipes"),
    path("authors/", authors, name="authors"),
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
