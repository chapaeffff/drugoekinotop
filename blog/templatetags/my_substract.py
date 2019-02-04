from django import template

register = template.Library()


@register.filter
def my_substract(value, arg):
    return value-arg
