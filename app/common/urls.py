from django.urls import path

from .views import detail_comment, report, tag

urlpatterns = [
    path(
        "api/comment/<int:pk>/<str:content_type>",
        detail_comment,
        name="api-detail-comment",
    ),
    path("api/report/<int:pk>/<str:content_type>", report, name="api-report"),
    path(
        "tag/<int:pk>/",
        tag,
        name="tag-detail",
    ),
]
