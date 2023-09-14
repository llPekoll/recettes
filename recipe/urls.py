from django.urls import path

from . import views

app_name = "recipe"

urlpatterns = [
    path("new/", views.new_recipe, name="new-recipe"),
]
