from article.models import Article
from django.core.paginator import Paginator
from django.shortcuts import render
from recipe.models import Recipe

from tools.translate import translate


def index(request):
    trans = translate(language="fr")
    articles = list(Article.objects.filter(is_published=False).order_by("-created_at"))
    recipes = list(Recipe.objects.filter(is_published=False).order_by("-created_at"))
    feed = sorted(articles + recipes, key=lambda x: x.created_at, reverse=True)
    paginator = Paginator(feed, 2)
    page_obj = paginator.get_page(1)

    return render(
        request,
        "index.html",
        {"trans": trans, "page_obj": page_obj},
    )


def page_recipes(request):
    recipes = Recipe.objects.filter(is_private=False)
    return render(
        request,
        "recipes_pages.html",
        {
            "recipes": recipes,
        },
    )


def page_articles(request):
    articles = Article.objects.filter(is_private=False)
    return render(
        request,
        "articles_page.html",
        {
            "articles": articles,
        },
    )


def about(request):
    return render(request, "footer_stuff/about.html")


def policy(request):
    return render(request, "footer_stuff/policy.html")


def terms(request):
    return render(request, "footer_stuff/terms.html")


def cookie(request):
    return render(request, "footer_stuff/cookie.html")
