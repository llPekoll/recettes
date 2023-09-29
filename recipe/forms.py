from django import forms
from django.forms.models import inlineformset_factory
from django.utils.text import slugify
from django_quill.forms import QuillFormField
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import default_storage

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
    ingredient_name = forms.CharField(
        max_length=100,
        required=True,
    )
    recipe_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = RecipeIngredient
        fields = ["quantity", "unit"]

    def save(self, commit=True):
        recipe_ingredient = super().save(commit=False)
        obj, created = Ingredient.objects.get_or_create(
            name=self.cleaned_data["ingredient_name"]
        )
        recipe = Recipe.objects.get(id=self.cleaned_data["recipe_id"])
        recipe_ingredient.unit = self.cleaned_data["unit"]
        recipe_ingredient.ingredient = obj
        recipe_ingredient.recipe = recipe
        if commit:
            recipe_ingredient.save()
        return recipe_ingredient


class RecipeForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[(category.value, category.name) for category in Category],
        required=False,
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
        choices=[(uom.value, uom.name) for uom in UnitOfMeasure], required=False
    )
    instructions = QuillFormField(required=False)
    recipe_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "duration",
            "duration_scale",
            "instructions",
            "category",
            "recipe_origin",
            "quantity",
            "youtube",
            "image",
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

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.category = self.cleaned_data["category"]
        recipe.duration_scale = self.cleaned_data["duration_scale"]
        recipe.recipe_origin = self.cleaned_data["recipe_origin"]
        recipe.image = self.cleaned_data["image"]

        slug = slugify(recipe.title)
        original_slug = slug
        count = 1
        while Recipe.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{count}"
            count += 1
        recipe.slug = slug
        if commit:
            recipe.save()
            storage = S3Boto3Storage()
            with default_storage.open(recipe.image.name, "rb") as f:
                storage.save(recipe.image.name, f)
                print("recipe.image.name")
                print(recipe.image.name)
                print(storage)
        return recipe
