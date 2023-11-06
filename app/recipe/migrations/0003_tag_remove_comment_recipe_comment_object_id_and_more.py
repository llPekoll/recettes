# Generated by Django 4.2.4 on 2023-11-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe", "0002_remove_comment_recipe_comment_content_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name="comment",
            name="recipe",
        ),
        migrations.AddField(
            model_name="comment",
            name="object_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(blank=True, to="recipe.tag"),
        ),
    ]
