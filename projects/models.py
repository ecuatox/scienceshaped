from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class Illustration(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(max_length=500, blank=True, verbose_name='Description')
    tags = models.CharField(max_length=500, blank=True, verbose_name='Tags')

    thumbnail = models.CharField(max_length=200, blank=True, verbose_name='Thumbnail')
    thumbnail_size = models.CharField(max_length=4, default=100, verbose_name='Thumbnail size (%)')

    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Publication date')

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    person = models.CharField(max_length=100, verbose_name='Person')
    message = models.CharField(max_length=500, verbose_name='Message')
    thumbnail = models.CharField(max_length=100, verbose_name='Thumbnail')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Publication date')

    def __str__(self):
        return self.title
