from article.models import Article
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from recipe.models import Recipe

from .models import Comment, Report, Tag


def detail_comment(request, pk, content_type):
    if request.method == "DELETE":
        # soft delete is better
        get_object_or_404(Comment, pk=pk)
        Comment.objects.filter(pk=pk).delete()
        comments = Comment.objects.all()
        return render(request, "comment_list.html", {"comments": comments})
    if content_type == "Article":
        content = get_object_or_404(Article, pk=pk)
    elif content_type == "Recipe":
        content = get_object_or_404(Recipe, pk=pk)
    if request.htmx:
        if request.method == "POST":
            Comment.objects.create(
                author=request.user,
                content_object=content,
                text=request.POST.get("comment"),
            )
            comments = content.comments.order_by("created_at")
            return render(request, "comment_list.html", {"comments": comments})


def tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    articles = tag.articles.filter(is_draft=False).order_by("-created_at")
    recipes = tag.recipes.filter(is_draft=False).order_by("-created_at")
    return render(
        request,
        "page_tags.html",
        {"articles": articles, "recipes": recipes, "tag": tag.name},
    )


def report(request, pk, content_type):
    """report a comment or an article or a recipe"""
    if content_type == "Article":
        content = get_object_or_404(Article, pk=pk)
    elif content_type == "Recipe":
        content = get_object_or_404(Recipe, pk=pk)
    elif content_type == "Comment":
        content = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        Report.objects.create(
            author=request.user,
            content_object=content,
            message=request.POST.get("message"),
        )
        return HttpResponse("Report posted", status=200)
