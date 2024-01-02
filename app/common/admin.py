from django.contrib import admin

from .models import Comment, Image, Link, Rate, Report


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "created_at")


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "type")
    ordering = ("-id",)


@admin.register(Report)
class AbuseAdmin(admin.ModelAdmin):
    list_display = ("id", "content_object", "created_at")
    ordering = ("-id",)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("id", "content_object")
    ordering = ("-id",)
