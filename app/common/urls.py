from django.urls import path

from .views import detail_comment, report, tag, link_list, link_detail, list_comment

urlpatterns = [
    path(
        "api/comment/<int:pk>/<str:content_type>",
        detail_comment,
        name="api-detail-comment",
    ),
    path(
        "api/comment/<str:content_type>",
        list_comment,
        name="api-list-comment",
    ),
    path(
        "api/link/<str:content_type>",
        link_list,
        name="api-link-list",
    ),
    path(
        "api/link/<int:pk>",
        link_detail,
        name="api-link-detail",
    ),
    path("api/report/<int:pk>/<str:content_type>", report, name="api-report"),
    path(
        "tag/<int:pk>/",
        tag,
        name="tag-detail",
    ),
]
