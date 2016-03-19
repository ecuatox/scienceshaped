from django.contrib import admin
from .models import Image

@admin.register(Image)
class IllustrationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Image', {
            'fields': [
                'title',
                'file',
            ]
        }),
        ('Meta', {
            'fields': [
                'time',
                'number',
            ]
        }),
    ]
    search_fields = [
        'title',
    ]
