from django.urls import path

from .views import detail_comment, report, tag_page

urlpatterns = [
    path(
        "comment/<int:pk>/<str:content_type>",
        detail_comment,
        name="detail-comment",
    ),
    path("report/<int:pk>/<str:content_type>", report, name="report"),
    path(
        "tag/<int:pk>/",
        tag_page,
        name="tag-page",
    ),
]
