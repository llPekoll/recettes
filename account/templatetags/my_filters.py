from django import template
from django.utils.translation import get_language_info

register = template.Library()


@register.filter
def clean_label_for_url(value):
    return value.replace(" ", "-").lower()


@register.filter
def language_name(code):
    return get_language_info(code)["name"]
