# Generated by Django 4.2.4 on 2023-12-08 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0006_remove_image_articles_remove_image_recipes_and_more"),
        ("article", "0003_remove_article_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to="common.image",
            ),
        ),
    ]