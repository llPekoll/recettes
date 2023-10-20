from django.shortcuts import render
from django.utils.translation import activate, get_language, gettext
from django.utils.translation import gettext_lazy as _

from recipe.models import Recipe


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext("Mamadou")
    finally:
        activate(cur_language)
    return text


def index(request):
    trans = translate(language="fr")
    recipes = Recipe.objects.filter(is_draft=False).order_by("-created_at")
    return render(request, "index.html", {"trans": trans, "recipes": recipes})
