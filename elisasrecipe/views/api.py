from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import render
from article.models import Article
from recipe.models import Recipe

from django.contrib.postgres.search import (
    SearchHeadline,
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)

def health(request):
    return JsonResponse({'status': 'ok'})

class FeedView(ListView):
    template_name = "feed.html"
    paginate_by = 2

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "feed.html"
        return "index.html"

    def get_queryset(self):
        articles = Article.objects.filter(is_published=False).order_by("-created_at")
        recipes = Recipe.objects.filter(is_published=False).order_by("-created_at")
        
        feed = sorted(list(articles) + list(recipes), key=lambda x: x.created_at, reverse=True)
        return feed

class FeedSearchView(ListView):
    template_name = "feed_search.html"
    paginate_by = 2

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return "feed_search.html"
        return "index.html"

    def get_queryset(self):
        search_query = self.request.GET.get("search","")
        vector = SearchVector("title", "description" )
        query = SearchQuery(search_query)
        search_headline = SearchHeadline("title", query)
        recipes = (
            Recipe.objects.annotate(
                rank=SearchRank(vector, query),
            )
            .annotate(headline=search_headline)
            .filter(rank__gte=0.00001)
            .order_by("-rank")[:2]
        )
        vector = SearchVector("title", "content" )
        articles = (
            Article.objects.annotate(
                rank=SearchRank(vector, query),
            )
            .annotate(headline=search_headline)
            .filter(rank__gte=0.00001)
            .order_by("-rank")[:2]
        )
        feed = sorted(list(articles) + list(recipes), key=lambda x: x.created_at, reverse=True)
        return feed


def search(request):
    print(request.POST)
    query_type = request.POST.get("type")
    search_query = request.POST.get("search")
    query = SearchQuery(search_query)
    search_headline = SearchHeadline("title", query)
    
    recipes = Recipe.objects.none()
    articles = Article.objects.none()
    if query_type == "recipes" or query_type =="all":
        vector = SearchVector("title", "description" )
        recipes = (
            Recipe.objects.annotate(
                rank=SearchRank(vector, query),
            )
            .annotate(headline=search_headline)
            .filter(rank__gte=0.00001)
            .order_by("-rank")[:2]
        )
    
    if query_type == "articles" or query_type =="all":
        vector = SearchVector("title", "content" )
        articles = (
            Article.objects.annotate(
                rank=SearchRank(vector, query),
            )
            .annotate(headline=search_headline)
            .filter(rank__gte=0.00001)
            .order_by("-rank")[:2]
        )
    
    feed = sorted(list(articles) + list(recipes), key=lambda x: x.created_at, reverse=True)
    return render(
        request,
        "feed_search.html",
        {"page_obj": feed},
    )

