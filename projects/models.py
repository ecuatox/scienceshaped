from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from files.models import Image

class Illustration(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    short = models.TextField(max_length=200, blank=True, verbose_name='Short Description')
    description = models.TextField(max_length=500, blank=True, verbose_name='Description')
    tags = models.CharField(max_length=500, blank=True, verbose_name='Tags')

    thumbnail = models.ForeignKey(Image, blank=True, null=True, related_name='%(app_label)s_%(class)s_related_thumb')
    thumbnail_size = models.CharField(max_length=4, default=100, verbose_name='Thumbnail size (%)')

    date = models.DateTimeField(default=timezone.now, verbose_name='Date')

    numberOfImages = models.IntegerField(verbose_name="Images")

    image1 = models.ForeignKey(Image, blank=True, null=True, related_name='%(app_label)s_%(class)s_related_img1', verbose_name='Image 1')
    image2 = models.ForeignKey(Image, blank=True, null=True, related_name='%(app_label)s_%(class)s_related_img2', verbose_name='Image 2')
    image3 = models.ForeignKey(Image, blank=True, null=True, related_name='%(app_label)s_%(class)s_related_img3', verbose_name='Image 3')

    def __str__(self):
        return self.title

    def short_lines(self):
        return self.short.split('\n')

    def description_lines(self):
        return self.description.split('\n')

class Testimonial(models.Model):
    person = models.CharField(max_length=100, verbose_name='Person')
    job = models.CharField(max_length=300, verbose_name='Job')
    message = models.CharField(max_length=1000, verbose_name='Message')
    thumbnail = models.ForeignKey(Image, blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='Publication date')

    def __str__(self):
        return self.person
