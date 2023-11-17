from enum import Enum

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField


class Category(Enum):
    RECIPE = "Recipe"
    HEALTH = "Health"
    COSMETIC = "Cosmetic"
    GARDEN = "Garden"
    HOME = "Home"
    FERMENTAION = "Fermentaion"
    ANIMAL = "Animal"
    JUICE = "Juice"


class Region(Enum):
    NORTH_AMERICA = "North America"
    SOUTH_AMERICA = "South America"
    EUROPE = "Europe"
    EASTERN_EUROPE = "Eastern Europe"
    WESTERN_EUROPE = "Western Europe"
    ASIA = "Asia"
    EAST_ASIA = "East Asia"
    SOUTH_ASIA = "South Asia"
    SOUTHEAST_ASIA = "Southeast Asia"
    AFRICA = "Africa"
    NORTH_AFRICA = "North Africa"
    SUB_SAHARAN_AFRICA = "Sub-Saharan Africa"
    OCEANIA = "Oceania"
    AUSTRALIA = "Australia"
    NEW_ZEALAND = "New Zealand"


class TimeScale(Enum):
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"
    YEAR = "Year"


class UnitOfMeasure(Enum):
    GRAMME = "Gramme"
    KILOGRAME = "Kilograme"
    SPOON = "Spoon"
    LITER = "Liter"
    ATINYBIT = "A tiny bit"
    PIECE = "Piece"


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="recipes"
    )
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(default=10)
    duration_scale = models.CharField(
        max_length=20,
        choices=[(TimeScale.value, TimeScale.name) for TimeScale in TimeScale],
        default=TimeScale.MINUTE.value,
    )

    instructions = QuillField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=20,
        choices=[(category.value, category.name) for category in Category],
        default=Category.RECIPE.value,
    )
    recipe_origin = models.CharField(
        max_length=20,
        choices=[(region.value, region.name) for region in Region],
        blank=True,
        null=True,
    )
    forks = models.ManyToManyField(
        "account.User", through="Fork", related_name="forked_recipes"
    )
    quantity = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )  # number of persons or number of usage
    youtube = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    tiktok = models.URLField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    url_link = models.URLField(max_length=255, null=True, blank=True)
    image = models.OneToOneField(
        "common.Image", on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField("common.Tag", related_name="recipes", blank=True)
    comments = GenericRelation("common.Comment")
    Report = GenericRelation("common.Report")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        original_slug = self.slug
        count = 1
        while Recipe.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{count}"
            count += 1
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_base64_or_svg = models.TextField(blank=True)
    recipes = models.ManyToManyField(Recipe, through="RecipeIngredient")

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, default=1, related_name="ingredients"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(
        max_length=20,
        choices=[(uom.value, uom.name) for uom in UnitOfMeasure],
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name}"

    @property
    def name(self):
        return self.ingredient.name


class Fork(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} forked {self.recipe.title}"
