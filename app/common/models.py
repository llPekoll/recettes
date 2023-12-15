from enum import Enum

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_quill.fields import QuillField
from pictures.models import PictureField
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storage(S3Boto3Storage):
    location = "media"


def image_upload_path(instance, filename):
    return f"{instance.type}_pictures/{filename}"


class Image(models.Model):
    PROFILE = "profile"
    ARTICLE = "article"
    RECIPE = "recipe"
    RECIPESTEP = "recipe step"
    TYPE_CHOICES = [
        (PROFILE, _("Profile")),
        (ARTICLE, _("Article")),
        (RECIPE, _("Recipe")),
        (RECIPESTEP, _("RecipeStep")),
    ]

    image = PictureField(
        upload_to=image_upload_path,
        aspect_ratios=[None, "1/1", "3/2", "16/9"],
        width_field="width",
        height_field="height",
        storage=CustomS3Boto3Storage(),
    )
    width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type} image {self.id}"


class Rate(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=3
    )

    def __str__(self):
        return f"{self.user.username} rates {self.content_object}: {self.value}"


class Comment(models.Model):
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    comment = QuillField()
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    edited = models.BooleanField(default=False)
    edtied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    report = GenericRelation("common.Report")

    def __str__(self):
        return f"{self.author.username} commented on {self.content_object}"


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class LinkType(Enum):
    YOUTUBE = "Youtube"
    TWITTER = "Twitter"
    INSTAGRAM = "Instagram"
    FACEBOOK = "Facebook"
    TIKTOK = "Tiktok"
    WEBSITE = "Website"


class Link(models.Model):
    value = models.URLField()
    type = models.CharField(
        max_length=20,
        choices=[(linkType.value, linkType.name) for linkType in LinkType],
        default=LinkType.YOUTUBE.value,
    )
    embedded = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.type}_{self.value}"


class Report(models.Model):
    author = models.ForeignKey(
        "account.User", related_name="author", on_delete=models.CASCADE
    )
    message = models.TextField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
