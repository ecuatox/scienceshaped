from django.contrib import admin
from .models import Illustration, Testimonial

@admin.register(Illustration)
class IllustrationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Illustration', {
            'fields': [
                'title',
                'short',
                'description',
                'tags',
                'hidden',
            ]
        }),
        ('Thumbnail', {
            'fields': [
                'thumbnail',
                'thumbnail_size',
            ]
        }),
        ('Images', {
            'fields': [
                'images'
            ]
        }),
        ('Article', {
            'fields': [
                'url',
                'pdf',
            ]
        }),
        ('Meta', {
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
                'person',
                'job',
                'message',
                'hidden',
            ]
        }),
        ('Meta', {
            'fields': [
                'date',
            ]
        }),
        ('Thumbnail', {
            'fields': [
                'thumbnail',
            ]
        }),
    ]
    search_fields = [
        'person',
    ]
