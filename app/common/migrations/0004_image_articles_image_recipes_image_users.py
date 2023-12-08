# Generated by Django 4.2.4 on 2023-12-08 05:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0003_remove_article_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipe", "0003_remove_recipe_image"),
        ("common", "0003_remove_comment_text_comment_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="articles",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="image",
                to="article.article",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="recipes",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="image",
                to="recipe.recipe",
            ),
        ),
        migrations.AddField(
            model_name="image",
            name="users",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile_picture",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
