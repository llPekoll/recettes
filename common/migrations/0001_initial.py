# Generated by Django 4.2.9 on 2024-01-04 12:26

import common.models
import django.core.validators
import django.db.models.deletion
import django_quill.fields
import versatileimagefield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                (
                    "image",
                    versatileimagefield.fields.VersatileImageField(
                        height_field="height",
                        storage=common.models.CustomS3Boto3Storage(),
                        upload_to=common.models.image_upload_path,
                        verbose_name="Image",
                        width_field="width",
                    ),
                ),
                (
                    "height",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Image Height"
                    ),
                ),
                (
                    "width",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Image Width"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("profile", "Profile"),
                            ("article", "Article"),
                            ("recipe", "Recipe"),
                            ("recipe step", "RecipeStep"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
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
        migrations.CreateModel(
            name="Report",
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
                ("message", models.TextField(blank=True, null=True)),
                ("object_id", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Rate",
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
                ("object_id", models.PositiveIntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "value",
                    models.IntegerField(
                        default=3,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Link",
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
                ("value", models.URLField()),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Youtube", "YOUTUBE"),
                            ("Twitter", "TWITTER"),
                            ("Instagram", "INSTAGRAM"),
                            ("Facebook", "FACEBOOK"),
                            ("Tiktok", "TIKTOK"),
                            ("Website", "WEBSITE"),
                        ],
                        default="Youtube",
                        max_length=20,
                    ),
                ),
                ("embedded", models.BooleanField(default=False)),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("object_id", models.PositiveIntegerField()),
                ("comment", django_quill.fields.QuillField()),
                ("edited", models.BooleanField(default=False)),
                ("edtied_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "parent_comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="common.comment",
                    ),
                ),
            ],
        ),
    ]
