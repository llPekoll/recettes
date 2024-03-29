# Generated by Django 4.2.9 on 2024-01-04 12:26

import django.db.models.deletion
import django_quill.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Fork",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("image_base64_or_svg", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("duration", models.IntegerField(default=10)),
                (
                    "duration_scale",
                    models.CharField(
                        choices=[
                            ("Minute", "MINUTE"),
                            ("Hour", "HOUR"),
                            ("Day", "DAY"),
                            ("Week", "WEEK"),
                            ("Month", "MONTH"),
                            ("Year", "YEAR"),
                        ],
                        default="Minute",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Recipe", "RECIPE"),
                            ("Health", "HEALTH"),
                            ("Cosmetic", "COSMETIC"),
                            ("Garden", "GARDEN"),
                            ("Home", "HOME"),
                            ("Fermentaion", "FERMENTAION"),
                            ("Animal", "ANIMAL"),
                            ("Juice", "JUICE"),
                        ],
                        default="Recipe",
                        max_length=20,
                    ),
                ),
                (
                    "recipe_origin",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("North America", "NORTH_AMERICA"),
                            ("South America", "SOUTH_AMERICA"),
                            ("Europe", "EUROPE"),
                            ("Eastern Europe", "EASTERN_EUROPE"),
                            ("Western Europe", "WESTERN_EUROPE"),
                            ("Asia", "ASIA"),
                            ("East Asia", "EAST_ASIA"),
                            ("South Asia", "SOUTH_ASIA"),
                            ("Southeast Asia", "SOUTHEAST_ASIA"),
                            ("Africa", "AFRICA"),
                            ("North Africa", "NORTH_AFRICA"),
                            ("Sub-Saharan Africa", "SUB_SAHARAN_AFRICA"),
                            ("Oceania", "OCEANIA"),
                            ("Australia", "AUSTRALIA"),
                            ("New Zealand", "NEW_ZEALAND"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                ("is_published", models.BooleanField(default=False)),
                ("is_private", models.BooleanField(default=False)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_draft", models.BooleanField(default=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "forks",
                    models.ManyToManyField(
                        related_name="forked_recipes",
                        through="recipe.Fork",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to="common.image",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, related_name="recipes", to="common.tag"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RecipeStep",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("step_number", models.IntegerField(default=1)),
                ("title", models.CharField(max_length=255)),
                ("instruction", django_quill.fields.QuillField(blank=True, null=True)),
                (
                    "image",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="common.image",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="steps",
                        to="recipe.recipe",
                    ),
                ),
            ],
            options={
                "ordering": ["step_number"],
            },
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "unit",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Gramme", "GRAMME"),
                            ("Kilograme", "KILOGRAME"),
                            ("Spoon", "SPOON"),
                            ("Liter", "LITER"),
                            ("A tiny bit", "ATINYBIT"),
                            ("Piece", "PIECE"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipe.ingredient",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ingredients",
                        to="recipe.recipe",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="ingredient",
            name="recipes",
            field=models.ManyToManyField(
                through="recipe.RecipeIngredient", to="recipe.recipe"
            ),
        ),
        migrations.AddField(
            model_name="fork",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="recipe.recipe"
            ),
        ),
        migrations.AddField(
            model_name="fork",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
