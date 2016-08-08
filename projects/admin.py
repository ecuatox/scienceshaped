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
        ('Images', {
            'fields': [
                'numberOfImages',
                'image1',
                'image2',
                'image3',
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
        ('Meta', {
            'fields': [
                'pub_date',
            ]
        })
    ]
    search_fields = [
        'title',
    ]
