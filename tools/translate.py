from django.utils.translation import activate, get_language, gettext


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = gettext("Mamadou")
    finally:
        activate(cur_language)
    return text
