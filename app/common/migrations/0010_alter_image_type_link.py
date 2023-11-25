# Generated by Django 4.2.4 on 2023-11-25 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('common', '0009_image_height_image_width_alter_image_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='type',
            field=models.CharField(choices=[('profile', 'Profile'), ('article', 'Article'), ('recipe', 'Recipe'), ('recipe step', 'RecipeStep')], max_length=20),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.URLField()),
                ('type', models.CharField(choices=[('Youtube', 'YOUTUBE'), ('Twitter', 'TWITTER'), ('Instagram', 'INSTAGRAM'), ('Facebook', 'FACEBOOK'), ('Tiktok', 'TIKTOK'), ('Website', 'WEBSITE')], default='Youtube', max_length=20)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]