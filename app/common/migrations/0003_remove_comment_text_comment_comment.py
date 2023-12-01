# Generated by Django 4.2.4 on 2023-12-01 21:16

import django_quill.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="text",
        ),
        migrations.AddField(
            model_name="comment",
            name="comment",
            field=django_quill.fields.QuillField(default="sako"),
            preserve_default=False,
        ),
    ]