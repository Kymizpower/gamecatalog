from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Разделяет строку по заданному разделителю"""
    if value:
        return value.split(arg)
    return []