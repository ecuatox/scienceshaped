from django import template

register = template.Library()

@register.filter(name='join_by')
def join_by(items, join_str):
    return join_str.join(map(str, items))
