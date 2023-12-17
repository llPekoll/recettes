from article.forms import ArticleForm
from article.models import Article
from common.forms import CommentForm
from common.models import Tag
from django.shortcuts import get_object_or_404, render


def page_article_creation(request):
    form = ArticleForm()
    tags = Tag.objects.all()
    return render(
        request,
        "new_article.html",
        {
            "create": True,
            "article": form,
            "tag_list": [tag.name for tag in tags],
        },
    )


def page_article_detail(request, pk):
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
            "comment_form": CommentForm(),
            "comments": comments,
        },
    )


def page_article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(instance=article)
    tags = article.tags.all()
    image = article.image.image.url
    return render(
        request,
        "edit_article.html",
        {
            "article": form,
            "tags": tags,
            "image": image,
        },
    )
