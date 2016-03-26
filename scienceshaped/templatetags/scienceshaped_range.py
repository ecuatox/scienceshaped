from django import template

register = template.Library()

@register.filter(name='toRange')
def toRange(length):
    return range(length)

@register.filter(name='toInvRange')
def toInvRange(length):
    return reversed(range(length))
