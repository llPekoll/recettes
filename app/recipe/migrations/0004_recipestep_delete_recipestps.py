# Generated by Django 4.2.4 on 2023-11-25 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_remove_recipe_facebook_remove_recipe_instagram_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255)),
                ('instruction', models.TextField()),
                ('recipe', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipe_step', to='recipe.recipe')),
            ],
        ),
        migrations.DeleteModel(
            name='RecipeStps',
        ),
    ]
