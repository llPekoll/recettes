from django.urls import path

from .views import (
    add_comment_article,
    article_creation,
    article_detail,
    article_edit,
    article_favorite,
)

app_name = "article"


urlpatterns = [
    path("new/", article_creation, name="new"),
    path("<int:pk>/", article_detail, name="detail"),
    path("<int:pk>/edit", article_edit, name="edit"),
    path("<int:pk>/favorite", article_favorite, name="favorite"),
    path("<int:pk>/comment", add_comment_article, name="add-comment"),
]
