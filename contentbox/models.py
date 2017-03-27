from django.db import models
from ckeditor.fields import RichTextField

class ContentBox(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', primary_key=True)
    content = RichTextField(default='')

    class Meta:
        verbose_name_plural = "contentboxes"

    def __str__(self):
        return self.title

    @staticmethod
    def get(title):
        try:
            return ContentBox.objects.get(title=title)
        except ContentBox.DoesNotExist:
            return ContentBox.objects.create(title=title)

    @staticmethod
    def getContent(title):
        return ContentBox.get(title).content
