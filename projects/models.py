import os
from django.db import models
from django.utils import timezone

from files.models import Image
from tags.models import Tag


class Illustration(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    short = models.TextField(max_length=200, blank=True, verbose_name='Short Description')
    description = models.TextField(max_length=500, blank=True, verbose_name='Description')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Tags')
    hidden = models.BooleanField(default=False, verbose_name='Hidden')

    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='URL')
    pdf = models.FileField(upload_to='pdfs', blank=True, null=True, verbose_name='PDF')

    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='%(app_label)s_%(class)s_related_thumb')
    thumbnail_size = models.CharField(max_length=4, default=100, verbose_name='Thumbnail size (%)')

    date = models.DateField(default=timezone.now, verbose_name='Date')

    images = models.ManyToManyField(Image, blank=True)

    @staticmethod
    def filter_tag(tag):
        if tag == 'all':
            return Illustration.objects.all()
        else:
            return Illustration.objects.filter(tags__label__contains=tag.lower())

    def __str__(self):
        return self.title

    def short_lines(self):
        return self.short.split('\n')

    def description_lines(self):
        return self.description.split('\n')

    def pdf_getname(self):
        return os.path.basename(self.pdf.name)


class IllustrationCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    tag = models.CharField(max_length=100, unique=True)
    thumb = models.ImageField(upload_to="categories")

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    person = models.CharField(max_length=100, verbose_name='Person')
    job = models.CharField(max_length=300, verbose_name='Job')
    message = models.CharField(max_length=1000, verbose_name='Message')
    hidden = models.BooleanField(default=False, verbose_name='Hidden')
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(default=timezone.now, verbose_name='Date')

    def __str__(self):
        return self.person
