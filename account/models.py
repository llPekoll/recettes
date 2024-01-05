from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify
from elisasrecipe import settings


class User(AbstractUser):
    favorite_recipes = models.ManyToManyField(
        "recipe.Recipe", related_name="favorite_recipes"
    )
    favorite_articles = models.ManyToManyField(
        "article.Article", related_name="favorite_articles"
    )
    bio = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, blank=True)
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
    comments = GenericRelation("common.Comment")
    tags = models.ManyToManyField("common.Tag", blank=True)
    links = models.ManyToManyField("common.Link", blank=True)
    profile_picture = models.ForeignKey(
        "common.Image",
        related_name="profile_pictures",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        user = User.objects.filter(slug=self.slug).exclude(id=self.id)
        if user.exists():
            slug, nb = self.slug.split("-")
            nb += 1
            self.slug = f"{slug}-{int(nb)}"
        super().save(*args, **kwargs)


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
