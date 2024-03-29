import json

from article.forms import ArticleForm
from article.models import Article
from common.models import Image, Link, Tag
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        write_article(form, request)
    if request.method == "DELETE":
        article.delete()
        return redirect(reverse("home"))


def article_creation(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        errors, content = write_article(form, request)
        if not errors:
            return HttpResponse(content, status=410)
        return redirect(reverse("article:detail", args=[content]))
    return HttpResponse("Method not allowed", status=405)


def write_article(form, request):
    print(request.POST, request.FILES)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        if request.POST.get("tags"):
            tags = json.loads(request.POST.get("tags"))
            for tag in tags:
                tag, _ = Tag.objects.get_or_create(name=tag.get("value"))
                article.tags.add(tag)
        # Links
        links = request.POST.get("links")
        links = json.loads(links)
        for link in links:
            Link.objects.create(
                content_object=article,
                value=link["linkValue"],
                type=link["linkType"],
                embedded=True if link["embeded"] == "on" else False,
            )
        # image default
        image = Image.objects.get(pk=15)
        if "image" in request.FILES:
            print(request.FILES["image"])
            image = Image(image=request.FILES["image"])
            image.save()
        article.image = image
        article.save()
        return True, article.id
    else:
        return False, form.errors


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
