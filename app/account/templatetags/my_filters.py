from decimal import Decimal

from django import template
from django.db.models import Avg
from django.utils.translation import get_language_info

register = template.Library()


@register.filter
def minio_to_localhost(value):
    return value.replace("minio:9000", "localhost:9000")


@register.filter
def total_rate_avg(content):
    return content.rates.all().aggregate(Avg("value"))["value__avg"] or 0


@register.filter
def total_rate_count(content):
    return content.rates.count()


@register.filter
def class_name(value):
    return value.__class__.__name__


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
    if number:
        number = Decimal(number)
        number = number.quantize(Decimal("1.00"))

        return number.normalize()
    return ""
