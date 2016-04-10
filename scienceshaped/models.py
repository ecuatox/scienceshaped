from django.db import models
from ckeditor.fields import RichTextField

class ContentBox(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    content = RichTextField(blank=True)

    def __str__(self):
        return self.title
