from django import forms
from django.utils.text import slugify
from django_quill.forms import QuillFormField

from .models import (
    Category,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeStep,
    Region,
    TimeScale,
    UnitOfMeasure,
)


class RecipeIngredientForm(forms.ModelForm):
    recipe = forms.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ["quantity", "unit"]

    def save(self, commit=True):
        recipe_ingredient = super().save(commit=False)
        obj, created = Ingredient.objects.get_or_create(
            name=self.cleaned_data["ingredient_name"]
        )
        print(self.cleaned_data)
        recipe = Recipe.objects.get(id=self.cleaned_data["recipe"])
        recipe_ingredient.unit = self.cleaned_data["unit"]
        recipe_ingredient.ingredient = obj
        recipe_ingredient.recipe = recipe
        if commit:
            recipe_ingredient.save()
        return recipe_ingredient


class RecipeStepForm(forms.ModelForm):
    step_number = forms.IntegerField(required=False)
    instruction = QuillFormField()
    image = forms.ImageField(required=False)

    class Meta:
        model = RecipeStep
        fields = ["title", "instruction", "step_number", "image", "recipe"]


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

    image = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "duration",
            "duration_scale",
            "category",
            "recipe_origin",
            "quantity",
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
        return recipe
