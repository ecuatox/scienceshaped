from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(x, y):
    return x*eval(y)

@register.filter(name='divide')
def divide(x, y):
    return x/eval(y)
