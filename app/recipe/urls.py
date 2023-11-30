from django.urls import path

from .views.api import (
    ingredient_detail,
    ingredient_list,
    step_detail,
    step_list,
    recipe_creation,
    recipe_edit,
    search_recipes,
    set_favorite,
    set_rating,
)
from .views.page import (
    page_edit_recipe,
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
    path("<int:pk>/edit/", page_edit_recipe, name="edit"),
    path("search/", page_search_recipes, name="search"),
    # API
    path("api/search/", search_recipes, name="api-search"),
    path("api/new", recipe_creation, name="api-new"),
    path("api/<int:pk>/edit/", recipe_edit, name="api-edit"),
    path("api/<int:pk>/rating/", set_rating, name="api-rating"),
    path("api/<int:pk>/favorite/", set_favorite, name="api-favorite"),
    path("api/ingredient/", ingredient_list, name="api-ingredient-list"),
    path("api/ingredient/<int:pk>/", ingredient_detail, name="api-ingredient-detail"),
    path("api/step/", step_list, name="api-step-list"),
    path("api/step/<int:pk>/", step_detail, name="api-step-detail"),
]
