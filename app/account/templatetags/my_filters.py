from django import template
from django.utils.translation import get_language_info

register = template.Library()


@register.filter
def clean_label_for_url(value):
    return value.replace(" ", "-").lower()


@register.filter
def name_for_form(value):
    return f"form{value.replace(' ' , '').lower()}"


@register.filter
def language_name(code):
    return get_language_info(code)["name"]


@register.filter
def format_date(date):
    return date.strftime("%d. %b %Y %I:%M%p")


@register.filter
def format_date_short(date):
    return date.strftime("%d %b %y %I:%M")


@register.filter
def clean_number(number):
    return number.normalize() if number else ""
