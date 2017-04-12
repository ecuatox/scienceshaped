import os
from django.conf import settings
from django.db import models
from django.utils import timezone

from tags.models import Tag


class Image(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    slug = models.CharField(max_length=100, default='', verbose_name='Slug')
    description = models.TextField(max_length=100, blank=True, verbose_name='Description')
    tags = models.ManyToManyField(Tag, verbose_name='Tags')
    time = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='images')
    number = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ("view_image_control_panel", "Can view image control panel"),
        )

    def __str__(self):
        if self.number > 1:
            return self.title + ' (' + str(self.number) + ')'
        return self.title

    def url(self):
        return '/media/' + str(self.file)

    @staticmethod
    def findId(slug):
        try:
            return Image.objects.filter(slug=slug).order_by('-time').first().number + 1
        except AttributeError:
            return 1

    @staticmethod
    def slugify(text):
        out = ''
        text = text.strip().lower().replace('_', ' ')
        for char in text:
            if char.isalnum() or char == ' ':
                out += char
        out = out.strip().replace(' ', '_')
        return out

    @staticmethod
    def fileExt(name):
        return name.split('.')[-1].lower()

    @staticmethod
    def saveImage(file, title, description, tags):
        slug = Image.slugify(title)
        number = Image.findId(slug)

        if number > 1:
            file.name = slug + '_' + str(number) + '.' + Image.fileExt(file.name)
        else:
            file.name = slug + '.' + Image.fileExt(file.name)

        instance = Image(file=file, title=title, slug=slug, description=description, number=number)
        instance.save()
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        return instance

    def renameImage(self, newtitle):
        slug = Image.slugify(newtitle)
        self.title = newtitle
        self.number = Image.findId(slug)
        oldpath = self.file.name
        directory = settings.MEDIA_ROOT
        ext = Image.fileExt(self.file.name)

        if self.number > 1:
            self.file.name = 'images/' + slug + '_' + str(self.number) + '.' + ext
        else:
            self.file.name = 'images/' + slug + '.' + ext

        # try:
        os.rename(directory + '/' + oldpath, directory + '/' + self.file.name)
        # except FileNotFoundError:
        #    pass

        self.save()
        return self
