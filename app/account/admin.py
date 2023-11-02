from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import PasswordResetToken, ProfileImage, ArticleImage, Article

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-id",)
    # actions = [delete_test_users]


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at")
    search_fields = ("user__username", "user__email", "token")
    ordering = ("-created_at",)


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image")
    ordering = ("-id",)


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image")
    ordering = ("-id",)


# class ArticleImageInline(admin.TabularInline):
#     model = ArticleImage


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_draft", "created_at")
    list_filter = ("is_draft", "created_at")
    search_fields = ("title", "author__username")
    # inlines = [ArticleImageInline]
