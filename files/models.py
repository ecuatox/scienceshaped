from django.db import models
from django.utils import timezone

class Image(models.Model):
    title = models.CharField(max_length=100, verbose_name='Filename')
    tags = models.CharField(max_length=100, verbose_name='Tags')
    time = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='images')
    number = models.IntegerField(default=0)

    def __str__(self):
        if self.number > 1:
            return self.title + " (" + str(self.number) + ")"
        return self.title
