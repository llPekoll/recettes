from django import template

register = template.Library()


@register.filter
def clean_label_for_url(value):
    return value.replace(" ", "-").lower()
