# Generated by Django 4.2.4 on 2023-11-02 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_alter_user_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="is_draft",
            field=models.BooleanField(default=True),
        ),
    ]
