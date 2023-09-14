# Generated by Django 4.2.4 on 2023-09-02 20:39

import storages.backends.s3boto3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_rename_youtube_channel_user_youtube_handle"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="https://f003.backblazeb2.com/file/Elisa-s-Corner/defaults/profile-default.png",
                null=True,
                storage=storages.backends.s3boto3.S3Boto3Storage(),
                upload_to="profile_pictures",
            ),
        ),
    ]
