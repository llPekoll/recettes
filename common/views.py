from article.models import Article
from common.forms import CommentForm, LinkForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from recipe.models import Recipe

from .models import Comment, Link, Report, Tag


def list_comment(request, pk, content_type):
    """Add comment to a content_type"""
    print("list_comment")
    if content_type == "Article":
        content = get_object_or_404(Article, pk=pk)
    elif content_type == "Recipe":
        content = get_object_or_404(Recipe, pk=pk)
    elif content_type == "Comment":
        content = get_object_or_404(Comment, pk=pk)
    if request.htmx:
        if request.method == "POST":
            print("request.POST")
            print(request.POST)
            form = CommentForm(request.POST)
            print(1)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.content_object = content
                comment.save()
            else:
                print(form.errors)
            comments = content.comments.order_by("created_at")
            print(comments)
            return render(request, "comment_list.html", {"comments": comments})


def detail_comment(request, pk):
    """Delete a coment or report a comment"""
    # TODO: add patch method
    if request.method == "DELETE":
        # soft delete is better
        get_object_or_404(Comment, pk=pk)
        Comment.objects.filter(pk=pk).delete()
        comments = Comment.objects.all()
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
    if content_type == "article":
        content = get_object_or_404(Article, pk=pk)
    elif content_type == "recipe":
        content = get_object_or_404(Recipe, pk=pk)
    elif content_type == "comment":
        content = get_object_or_404(Comment, pk=pk)

    if request.method == "POST":
        Report.objects.create(
            author=request.user,
            content_object=content,
            message=request.POST.get("message"),
        )
        return HttpResponse("Report posted", status=200)


# TODO: maybe merge this 2 function into a get_or_create
def link_list(request, content_type):
    if content_type == "article":
        content = get_object_or_404(Article, pk=request.POST.get("article"))
    elif content_type == "recipe":
        content = get_object_or_404(Recipe, pk=request.POST.get("recipe"))
    elif content_type == "user":
        content = get_object_or_404("account.User", pk=request.POST.get("user"))
    if request.method == "POST":
        print(request.POST)
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.author = request.user
            link.content_object = content
            link.save()
        else:
            print(form.errors)
        links = content.links.all()
        return render(
            request, "patterns/components/link_list/link_list.html", {"links": links}
        )
    return """ link added """


def link_detail(request, pk, content_type):
    if content_type == "Article":
        content = get_object_or_404(Article, pk=pk)
    elif content_type == "Recipe":
        content = get_object_or_404(Recipe, pk=pk)
    elif content_type == "User":
        content = get_object_or_404("account.User", pk=pk)
    Link.objects.get(
        content_type=content,
        pk=pk,
        value=request.POST.get("value"),
        type=request.POST.get("type"),
    )
    return """ link updated """
