from django.urls import path

from .views import add_new_comment_article  # go_to_new_article,
from .views import article_creation, article_detail, article_favorite

urlpatterns = [
    # Basic auth
    # path("new-article/", go_to_new_article, name="new-article"),
    path("article_creation/", article_creation, name="article-creation"),
    path("article/<int:pk>/", article_detail, name="article-detail"),
    path("article/<int:pk>/favorite", article_favorite, name="article-favorite"),
    path(
        "article/<int:pk>/comment/new",
        add_new_comment_article,
        name="article-comment-new",
    ),
]
