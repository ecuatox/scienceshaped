from django.contrib import admin

from .models import Tag, TagGroup

admin.site.register(Tag)
admin.site.register(TagGroup)
