from django.urls import path

from .views import (
    add_comment_article,
    article_creation,
    article_detail,
    article_edit,
    article_favorite,
)

urlpatterns = [
    path("article_creation/", article_creation, name="article-creation"),
    path("article/<int:pk>/", article_detail, name="article-detail"),
    path("article/<int:pk>/edit", article_edit, name="article-edit"),
    path("article/<int:pk>/favorite", article_favorite, name="article-favorite"),
    path(
        "article/<int:pk>/comment",
        add_comment_article,
        name="article-comment-new",
    ),
]
