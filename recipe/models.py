from enum import Enum

from django.db import models


class Category(Enum):
    RECIPE = "recipe"
    HEALTH = "health"
    COSMETIC = "cosmetic"


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    author = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="recipes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=20,
        choices=[(category.value, category.name) for category in Category],
        default=Category.RECIPE.value,
    )
    likes = models.ManyToManyField(
        "account.User", through="Like", related_name="liked_recipes"
    )
    forks = models.ManyToManyField(
        "account.User", through="Fork", related_name="forked_recipes"
    )
    quantity = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )  # number of persons or number of usage
    youtube_link = models.CharField(max_length=255, null=True, blank=True)
    # image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    recipes = models.ManyToManyField(Recipe, through="RecipeIngredient")

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name} for {self.recipe.title}"


class Like(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"


class Comment(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.recipe.title}"


class Fork(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} forked {self.recipe.title}"
