from django.contrib import admin

from .models import Comment, Image, Rate


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created_at")
    # list_filter = ("title",)


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "type")
    ordering = ("-id",)