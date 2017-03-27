from django.contrib import admin
from .models import ContentBox

@admin.register(ContentBox)
class ContentBoxAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Contentbox', {
            'fields': [
                'title',
                'content',
            ]
        }),
    ]
