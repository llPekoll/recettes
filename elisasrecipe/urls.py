from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from .views.api import (
    FeedSearchView,
    FeedView,
    health,
    search,
)
from .views.page import about, cookie, index, policy, terms


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),
    # path("", include("django_backblaze_b2.urls")),
]
if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]

urlpatterns += i18n_patterns(
    path("", index, name="home"),
    path("cookie/", cookie, name="cookie"),
    path("policy/", policy, name="policy"),
    path("terms/", terms, name="terms"),
    path("about/", about, name="about"),
    path("recipes/", about, name="page-recipes"),
    path("articles/", about, name="page-articles"),
    path("authors/", about, name="page-authors"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("feed/search", FeedSearchView.as_view(), name="feed-search"),
    path("api/search/<str:content_type>", search, name="api-search"),
    path("", include("account.urls")),
    path("article/", include("article.urls")),
    path("", include("common.urls")),
    path("recipe/", include("recipe.urls")),
)
