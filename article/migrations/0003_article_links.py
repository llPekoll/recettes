# Generated by Django 4.2.4 on 2024-01-25 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('article', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.link'),
        ),
    ]