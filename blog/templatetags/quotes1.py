from django import template

register = template.Library()

@register.filter
def quotes1(value):
    value.replace("\"", "\"")
    value.replace("«", "\"")
    value.replace("»", "\"")
    value.replace("<<", "\"")
    value.replace(">>", "\"")

    return value