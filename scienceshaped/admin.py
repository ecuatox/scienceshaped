from django import forms
from django.contrib import admin

from .models import ContentBox

@admin.register(ContentBox)
class ContentBoxAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Content box', {
            'fields': [
                'title',
                'content',
            ]
        }),
    ]
