from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storage(S3Boto3Storage):
    location = "media"


def image_upload_path(instance, filename):
    return f"{instance.type}_pictures/{filename}"


class Image(models.Model):
    PROFILE = "profile"
    ARTICLE = "article"
    RECIPE = "recipe"
    TYPE_CHOICES = [
        (PROFILE, _("Profile")),
        (ARTICLE, _("Article")),
        (RECIPE, _("Recipe")),
    ]

    image = models.ImageField(
        upload_to=image_upload_path, storage=CustomS3Boto3Storage()
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type} image"


class Rate(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    recipe = models.ForeignKey("recipe.Recipe", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=3
    )

    def __str__(self):
        return f"{self.user.username} rates {self.recipe.title}: {self.value}"


class Comment(models.Model):
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    text = models.TextField()
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    edited = models.BooleanField(default=False)
    edtied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} commented on {self.content_object}"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    # TODO::

    def __str__(self):
        return self.name
