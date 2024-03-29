from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_draft", "created_at", "slug", "id")
    readonly_fields = ("id",)
    list_filter = ("is_draft", "created_at")
    search_fields = ("title", "author__username", "id")
