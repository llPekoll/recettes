# Generated by Django 4.2.4 on 2023-12-08 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="profile_picture",
        ),
    ]
