from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='settings_value')
def settings_value(name):
    return getattr(settings, name, "")
