import json

from article.forms import ArticleForm
from article.models import Article
from common.models import Comment, Image, Tag
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


def article_creation(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
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
            return redirect(reverse("article-detail", args=[article.id]))
        else:
            # TODO:
            # not allow to get there block it from the front!
            print(form.errors)
    return redirect(reverse("my-articles"))


def article_favorite(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)
    if article in user.favorite_articles.all():
        print("remove")
        user.favorite_articles.remove(article)
        is_favorite = False
    else:
        user.favorite_articles.add(article)
        is_favorite = True
        print("add")
    return render(
        request,
        "is_favorite.html",
        {"recipe": article, "is_favorite": is_favorite},
    )


def add_comment_article(request, pk):
    if request.htmx:
        if request.method == "POST":
            article = get_object_or_404(Article, pk=pk)
            Comment.objects.create(
                author=request.user,
                content_object=article,
                text=request.POST.get("comment"),
            )
            comments = article.comments.order_by("created_at")
            return render(request, "comment_list.html", {"comments": comments})


def article_detail(request, pk):
    user = request.user
    article = get_object_or_404(Article, pk=pk)
    is_favorite = article in user.favorite_articles.all()
    is_author = article.author == user
    comments = article.comments.all().order_by("created_at")
    return render(
        request,
        "article_detail.html",
        {
            "article": article,
            "is_author": is_author,
            "is_favorite": is_favorite,
            "comments": comments,
        },
    )


def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(instance=article)
    return render(
        request,
        "edit_article.html",
        {
            "article": form,
        },
    )
