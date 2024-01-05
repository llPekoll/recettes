from article.models import Article
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.translation import activate, get_language, gettext
from django.views.generic import ListView
from recipe.models import Recipe


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext("Mamadou")
    finally:
        activate(cur_language)
    return text


def cookie(request):
    print("cookie")
    i = render(request, "cookie.html")
    print(dir(i))
    print(i.content)
    return render(request, "cookie.html")


def index(request):
    trans = translate(language="fr")
    articles = list(Article.objects.filter(is_published=False).order_by("-created_at"))
    recipes = list(Recipe.objects.filter(is_published=False).order_by("-created_at"))
    feed = sorted(articles + recipes, key=lambda x: x.created_at, reverse=True)
    print(feed)
    paginator = Paginator(feed, 2)
    print(paginator)
    page_obj = paginator.get_page(1)
    print(page_obj)

    return render(
        request,
        "index.html",
        {"trans": trans, "page_obj": page_obj},
    )


class FeedView(ListView):
    template_name = "feed.html"
    paginate_by = 2

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "feed.html"
        return "index.html"

    def get_queryset(self):
        articles = list(
            Article.objects.filter(is_published=False).order_by("-created_at")
        )
        recipes = list(
            Recipe.objects.filter(is_published=False).order_by("-created_at")
        )
        feed = sorted(articles + recipes, key=lambda x: x.created_at, reverse=True)
        return feed
