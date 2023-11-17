from django.urls import path

from .views import (
    ingredient_list,
    add_new_comment,
    add_recipe_tags,
    authors,
    ingredient_detail,
    edit_recipe,
    recipe_creation,
    recipe_detail,
    recipe_favorite,
    recipe_rating,
    recipes,
    search_recipes,
)

app_name = "recipe"

urlpatterns = [
    path("new/", recipe_creation, name="new"),
    path("recipe/<int:pk>/", recipe_detail, name="recipe-detail"),
    path("recipe/<int:pk>/favorite", recipe_favorite, name="recipe-favorite"),
    path("recipe/<int:pk>/rating", recipe_rating, name="recipe-rating"),
    path("recipe/<int:pk>/comment/new", add_new_comment, name="recipe-comment-new"),
    path("recipe/<int:pk>/tags/", add_recipe_tags, name="add_recipe_tags"),
    path("recipe/<int:pk>/edit/", edit_recipe, name="edit_recipe"),
    path("recipes/search/", search_recipes, name="recipe-search"),
    path("", recipes, name="list-page"),
    path("authors/", authors, name="authors"),
    # mix add and delete ingredient with post and delete
    path("ingredient/", ingredient_list, name="ingredient-list"),
    path("ingredient/<int:pk>/", ingredient_detail, name="ingredient-detail"),
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
