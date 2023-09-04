from django import template

register = template.Library()

@register.filter
def replace_space_with_dash(value):
    return value.replace(' ', '-')