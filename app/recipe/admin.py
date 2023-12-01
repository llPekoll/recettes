from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, RecipeStep


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("__str__", "author", "created_at", "pk")
    list_filter = ("title",)
    search_fields = ("title", "author")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["created_at"]
    inlines = [RecipeIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe",)
