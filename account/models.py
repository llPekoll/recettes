from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.db import models


class User(AbstractUser):
    favorite_recipes = models.ManyToManyField(
        "recipe.Recipe", related_name="favorited_by"
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
    # TODO: add profile image, bio, etc.

    def __str__(self):
        return self.username

    # pass
