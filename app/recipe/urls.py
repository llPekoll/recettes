from django.urls import path

from .views.api import ingredient_detail, ingredient_list, set_favorite, set_rating
from .views.page import (
    page_recipe_creation,
    page_recipe_detail,
    page_recipes,
    page_search_recipes,
)

app_name = "recipe"

urlpatterns = [
    # Pages
    path("", page_recipes, name="list"),
    path("new/", page_recipe_creation, name="new"),
    path("<int:pk>/", page_recipe_detail, name="detail"),
    path("<int:pk>/edit/", page_recipe_creation, name="edit"),
    path("search/", page_search_recipes, name="search"),
    # API
    path("api/<int:pk>/favorite/", set_favorite, name="api-favorite"),
    path("api/<int:pk>/rating/", set_rating, name="api-rating"),
    path("api/ingredient/", ingredient_list, name="api-ingredient-list"),
    path("api/ingredient/<int:pk>/", ingredient_detail, name="api-ingredient-detail"),
]
