from django.contrib import admin
from .models import Illustration

@admin.register(Illustration)
class IllustrationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Illustration', {
            'fields': [
                'title',
                'description',
                'tags',
            ]
        }),
        ('Thumbnail', {
            'fields': [
                'thumbnail',
                'thumbnail_size',
            ]
        }),
        ('Published', {
            'fields': [
                'pub_date',
            ]
        })
    ]
    search_fields = [
        'title',
    ]
