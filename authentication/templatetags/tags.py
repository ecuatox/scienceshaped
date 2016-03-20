from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='inGroup')
def inGroup(user, groupName):
    return user.groups.filter(name=groupName).exists()
