from django import forms
from django.forms.models import inlineformset_factory
from django.utils.text import slugify
from django_quill.forms import QuillFormField

from .models import (
    Category,
    Ingredient,
    UnitOfMeasure,
    Recipe,
    RecipeIngredient,
    Region,
    TimeScale,
)


class RecipeIngredientForm(forms.ModelForm):
    unit = forms.ChoiceField(
        choices=[(uom.value, uom.name) for uom in UnitOfMeasure],
    )
    ingredient_name = forms.CharField(
        max_length=100,
        required=True,
    )
    recipe = forms.ModelForm

    class Meta:
        model = RecipeIngredient
        fields = ["quantity", "recipe"]

    def save(self, commit=True):
        recipe_ingredient = super().save(commit=False)
        obj, created = Ingredient.objects.get_or_create(
            name=self.cleaned_data["ingredient_name"]
        )
        recipe = Recipe.objects.get(id=self.cleaned_data["recipe"].id)
        recipe_ingredient.unit = self.cleaned_data["unit"]
        recipe_ingredient.ingredient = obj
        recipe_ingredient.recipe = recipe
        if commit:
            recipe_ingredient.save()
        return recipe_ingredient


class RecipeForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[(category.value, category.name) for category in Category]
    )
    recipe_origin = forms.ChoiceField(
        choices=[(region.value, region.name) for region in Region], required=False
    )
    duration_scale = forms.ChoiceField(
        choices=[(timeScale.value, timeScale.name) for timeScale in TimeScale],
        required=False,
    )
    # keep this one in order to have the select in for html form
    unit = forms.ChoiceField(
        choices=[(uom.value, uom.name) for uom in UnitOfMeasure],
    )
    instructions = QuillFormField()

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "duration",
            "instructions",
            "category",
            "recipe_origin",
            "quantity",
            "youtube",
            "is_published",
            "is_private",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {
            "duration": "Duration (in minutes)",
            "recipe_origin": "Recipe Origin (optional)",
            "is_published": "Publish Recipe",
            "is_private": "Make Recipe Private",
        }
        help_texts = {
            "description": "Enter a brief description of the recipe",
            "recipe_origin": "Enter the origin of the recipe (optional)",
            "is_published": "Check this box to publish the recipe",
            "is_private": "Check this box to make the recipe private",
        }
        error_messages = {
            "title": {
                "required": "Please enter a title for the recipe",
            },
        }

    def clean_title(self):
        # Generate a slug if one is not provided
        title = self.cleaned_data["title"]
        slug = self.cleaned_data.get("slug")
        if not slug:
            slug = slugify(title)
        return title

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.save()
        return recipe
