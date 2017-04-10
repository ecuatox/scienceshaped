from django.db import models
from django.utils import timezone


class TagGroup(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Title')
    creation_date = models.DateTimeField(default=timezone.now, verbose_name='Creation Date')

    def __str__(self):
        return self.title


class Tag(models.Model):
    label = models.CharField(max_length=100, verbose_name='Label')
    group = models.ForeignKey(TagGroup, verbose_name='Group')
    creation_date = models.DateTimeField(default=timezone.now, verbose_name='Creation Date')

    class Meta:
        permissions = (
            ("view_tag_control_panel", "Can view tag control panel"),
        )
        unique_together = ('label', 'group')

    def __str__(self):
        return self.label

    @staticmethod
    def clean_tags(tags):
        cleaned = []
        for tag in tags.split(','):
            try:
                cleaned.append(int(tag.strip()))
            except ValueError:
                pass
        return cleaned

    @staticmethod
    def stringlist(manager):
        tags = manager.all()
        return ', '.join([tag.label for tag in tags])
