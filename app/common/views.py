from article.models import Article
from django.shortcuts import get_object_or_404, render
from recipe.models import Recipe

from .models import Comment, Tag


def detail_comment(request, pk, content_type):
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

        if request.method == "DELETE":
            # soft delete is better
            get_object_or_404(Comment, pk=pk)
            Comment.objects.filter(pk=pk).delete()
            comments = Comment.objects.all()
            return render(request, "comment_list.html", {"comments": comments})


def tag_page(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    articles = tag.articles.all()
    recipes = tag.recipes.all()
    return render(
        request,
        "page_tags.html",
        {"articles": articles, "recipes": recipes, "tag": tag.name},
    )
