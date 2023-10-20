from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django_quill.fields import QuillField

from elisasrecipe import settings


class User(AbstractUser):
    favorite_recipes = models.ManyToManyField(
        "recipe.Recipe", related_name="favorited_by"
    )
    # Socials
    youtube_handle = models.URLField(blank=True)
    twitter_handle = models.URLField(blank=True)
    instagram_handle = models.URLField(blank=True)
    facebook_handle = models.URLField(blank=True)
    tiktok_handle = models.URLField(blank=True)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures",
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="myapp_user_groups",  # specify a custom related name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="myapp_user_permissions",  # specify a custom related name
        related_query_name="user",
    )

    def __str__(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=200)
    # ?? slug ??
    content = QuillField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    edited = models.BooleanField(default=False)
    edtied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    image = models.ImageField(
        upload_to="blog_images",
        storage=S3Boto3Storage(),
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    # this one can be usefull for share btn
    # def get_absolute_url(self):
    #     return reverse("blog_entry_detail", args=[str(self.id)])


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
