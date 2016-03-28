from django.contrib import admin
from .models import Illustration, Testimonial

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
                'date',
            ]
        })
    ]
    search_fields = [
        'title',
    ]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Testimonial', {
            'fields': [
                'title',
                'person',
                'message',
            ]
        }),
        ('Thumbnail', {
            'fields': [
                'thumbnail',
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
