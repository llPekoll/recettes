from django.urls import path

from .views import detail_comment, tag_page

urlpatterns = [
    path(
        "comment/<int:pk>/<str:content_type>",
        detail_comment,
        name="detail-comment",
    ),
    path(
        "tag/<int:pk>/",
        tag_page,
        name="tag-page",
    ),
]
