import json

from article.forms import ArticleForm
from article.models import Article
from common.models import Image, Tag
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


def article_edit(request, pk):
    if request.method == "POST":
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(request.POST, instance=article)
        write_article(form, request)


def article_creation(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        write_article(form, request)


def write_article(form, request):
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        if "tags" in request.POST:
            tags = json.loads(request.POST.get("tags"))
            for tag in tags:
                tag, _ = Tag.objects.get_or_create(name=tag.get("value"))
                article.tags.add(tag)
        if "image" in request.FILES:
            image = Image(image=request.FILES["image"])
            image.save()
            article.image = image
        article.save()
        return redirect(reverse("article:detail", args=[article.id]))
    else:
        # TODO:
        # tell user something went wrong
        print(form.errors)


def set_favorite(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)
    if article in user.favorite_articles.all():
        user.favorite_articles.remove(article)
        is_favorite = False
    else:
        user.favorite_articles.add(article)
        is_favorite = True
    return render(
        request,
        "is_favorite.html",
        {"recipe": article, "is_favorite": is_favorite},
    )
