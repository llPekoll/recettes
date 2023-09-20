from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("title",)
    search_fields = ("title", "author")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["created_at"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass
