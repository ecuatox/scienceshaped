from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

class Illustration(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(max_length=500, blank=True, verbose_name='Description')
    tags = models.CharField(max_length=500, blank=True, verbose_name='Tags')

    thumbnail = models.CharField(max_length=200, blank=True, verbose_name='Thumbnail')
    thumbnail_size = models.CharField(max_length=4, default=100, verbose_name='Thumbnail size (%)')

    date = models.DateTimeField(default=timezone.now, verbose_name='Date')

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    person = models.CharField(max_length=100, verbose_name='Person')
    job = models.CharField(max_length=300, verbose_name='Job')
    message = models.CharField(max_length=1000, verbose_name='Message')
    thumbnail = models.CharField(max_length=100, verbose_name='Thumbnail')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Publication date')

    def __str__(self):
        return self.person
