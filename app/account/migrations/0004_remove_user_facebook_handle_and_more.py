# Generated by Django 4.2.4 on 2023-11-25 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_alter_image_type_link'),
        ('account', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='facebook_handle',
        ),
        migrations.RemoveField(
            model_name='user',
            name='instagram_handle',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tiktok_handle',
        ),
        migrations.RemoveField(
            model_name='user',
            name='twitter_handle',
        ),
        migrations.RemoveField(
            model_name='user',
            name='website',
        ),
        migrations.RemoveField(
            model_name='user',
            name='youtube_handle',
        ),
        migrations.AddField(
            model_name='user',
            name='links',
            field=models.ManyToManyField(blank=True, to='common.link'),
        ),
    ]
