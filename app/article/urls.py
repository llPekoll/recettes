from django.urls import path

from .views.api import article_creation, article_edit, set_favorite
from .views.page import page_article_creation, page_article_detail, page_article_edit

app_name = "article"


urlpatterns = [
    # Pages
    path("new/", page_article_creation, name="new"),
    path("<int:pk>/", page_article_detail, name="detail"),
    path("<int:pk>/edit/", page_article_edit, name="edit"),
    # API
    path("api/", article_creation, name="api-new"),
    path("api/<int:pk>/", article_edit, name="api-edit"),
    path("api/<int:pk>/favorite/", set_favorite, name="api-set-favorite"),
]
