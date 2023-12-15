# Generated by Django 4.2.4 on 2023-12-15 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('common', '0006_remove_image_articles_remove_image_recipes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='recipe',
        ),
        migrations.AddField(
            model_name='rate',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='rate',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
