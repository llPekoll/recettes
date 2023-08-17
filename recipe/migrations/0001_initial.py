# Generated by Django 4.2.4 on 2023-08-14 16:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("account", "0001_initial"),
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
            ],
        ),
        migrations.CreateModel(
            name="Like",
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
                ("description", models.TextField()),
                ("instructions", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("recipe", "RECIPE"),
                            ("medicine", "MEDICINE"),
                            ("cosmetic", "COSMETIC"),
                        ],
                        default="recipe",
                        max_length=20,
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "youtube_link",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("is_published", models.BooleanField(default=False)),
                ("is_private", models.BooleanField(default=False)),
                ("is_featured", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recipes",
                        to="account.user",
                    ),
                ),
                (
                    "forks",
                    models.ManyToManyField(
                        related_name="forked_recipes",
                        through="recipe.Fork",
                        to="account.user",
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(
                        related_name="liked_recipes",
                        through="recipe.Like",
                        to="account.user",
                    ),
                ),
            ],
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
                ("unit", models.CharField(max_length=50)),
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
                        on_delete=django.db.models.deletion.CASCADE, to="recipe.recipe"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="like",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="recipe.recipe"
            ),
        ),
        migrations.AddField(
            model_name="like",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="account.user"
            ),
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
                on_delete=django.db.models.deletion.CASCADE, to="account.user"
            ),
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "parent_comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="recipe.comment",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="recipe.recipe",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="account.user"
                    ),
                ),
            ],
        ),
    ]