from django import forms
from .models import Recipe, Category, Region, Ingredient, RecipeIngredient


class IngredientForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}))

    class Meta:
        model = Recipe
        fields = [
            "name",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {
            "name": "Ingredient Name",
            "description": "Description",
        }
        help_texts = {
            "name": "Enter the name of the ingredient",
            "description": "Enter a description for the ingredient",
        }
        error_messages = {
            "name": {
                "required": "Please enter a name for the ingredient",
            },
            "description": {
                "required": "Please enter a description for the ingredient",
            },
        }


class RecipeIngredientForm(forms.Form):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all())
    quantity = forms.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = RecipeIngredient
        fields = [
            "ingredient",
            "quantity",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {
            "ingredient": "Ingredient",
            "quantity": "Quantity",
        }
        help_texts = {
            "ingredient": "Select an ingredient",
            "quantity": "Enter the quantity of the ingredient",
        }
        error_messages = {
            "ingredient": {
                "required": "Please select an ingredient",
            },
            "quantity": {
                "required": "Please enter a quantity for the ingredient",
            },
        }


class RecipeForm(forms.ModelForm):
    recipe_ingredients = forms.inlineformset_factory(
        Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=1, can_delete=True
    )
    category = forms.ChoiceField(
        choices=[(category.value, category.name) for category in Category]
    )
    recipe_origin = forms.ChoiceField(
        choices=[(region.value, region.name) for region in Region], required=False
    )

    class Meta:
        model = Recipe
        fields = [
            "title",
            "slug",
            "description",
            "durations",
            "instructions",
            "author",
            "category",
            "recipe_origin",
            "likes",
            "forks",
            "quantity",
            "youtube_link",
            "is_published",
            "is_private",
            "is_featured",
            "url_link",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "instructions": forms.Textarea(attrs={"rows": 10}),
        }
        labels = {
            "durations": "Duration (in minutes)",
            "recipe_origin": "Recipe Origin (optional)",
            "is_published": "Publish Recipe",
            "is_private": "Make Recipe Private",
            "is_featured": "Feature Recipe",
            "url_link": "URL Link (optional)",
            "image": "Image (optional)",
        }
        help_texts = {
            "description": "Enter a brief description of the recipe",
            "instructions": "Enter the instructions for the recipe",
            "recipe_origin": "Enter the origin of the recipe (optional)",
            "is_published": "Check this box to publish the recipe",
            "is_private": "Check this box to make the recipe private",
            "is_featured": "Check this box to feature the recipe",
            "url_link": "Enter a URL link for the recipe (optional)",
            "image": "Upload an image for the recipe (optional)",
        }
        error_messages = {
            "title": {
                "required": "Please enter a title for the recipe",
            },
            "description": {
                "required": "Please enter a description for the recipe",
            },
            "durations": {
                "required": "Please enter a duration for the recipe",
            },
            "instructions": {
                "required": "Please enter instructions for the recipe",
            },
        }

    # author = forms.ModelChoiceField(queryset=User.objects.all())
    # likes = forms.ModelMultipleChoiceField(queryset=User.objects.count())
    # forks = forms.ModelMultipleChoiceField(queryset=User.objects.all())
