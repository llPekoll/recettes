from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        print(get_language())
        print(language)
        text = gettext("hello")
        print(text)
        text = gettext("French")
        text = gettext("Mamadou")
    finally:
        activate(cur_language)
    return text


def index(request):
    trans = translate(language="fr")
    print("trou de balle")
    return render(request, "index.html", {"trans": trans})
