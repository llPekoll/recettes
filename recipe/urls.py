from django.urls import path

from .views import (  # RecipeViewSet,; IngredientViewSet,; AddIngredientView,; DeleteIngredientView,
    add_ingredient,
    new_recipe,
)

# recipe_list = RecipeViewSet.as_view({"get": "list", "post": "create"})
# recipe_detail = RecipeViewSet.as_view(
#     {"get": "retrieve", "put": "update", "delete": "destroy"}
# )

# ingredient_list = IngredientViewSet.as_view({"get": "list", "post": "create"})
# ingredient_detail = IngredientViewSet.as_view(
#     {"get": "retrieve", "put": "update", "delete": "destroy"}
# )

urlpatterns = [
    path("new-recipe/", new_recipe, name="new-recipe"),
    path("add-ingredient/", add_ingredient, name="add-ingredient"),
    # path("recipes/", recipe_list, name="recipe-list"),
    # path("recipes/<int:pk>/", recipe_detail, name="recipe-detail"),
    # path("ingredients/", ingredient_list, name="ingredient-list"),
    # path("ingredients/<int:pk>/", ingredient_detail, name="ingredient-detail"),
    # path(
    #     "recipes/<int:pk>/add-ingredient/",
    #     AddIngredientView.as_view(),
    #     name="add_ingredient",
    # ),
    # path(
    #     "ingredients/<int:pk>/delete/",
    #     DeleteIngredientView.as_view(),
    #     name="delete_ingredient",
    # ),
]
