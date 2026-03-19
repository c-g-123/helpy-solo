from django.core.exceptions import ValidationError
from django.db import models

from .task import Task


def task_resource_upload_path(instance, filename):
    return f'task_resources/task_{instance.task.id}/{filename}'


class Resource(models.Model):

    MAX_NAME_LENGTH = 255

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='resources'
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    file = models.FileField(
        upload_to=task_resource_upload_path,
        null=True,
        blank=True
    )
    link = models.URLField(
        null=True,
        blank=True
    )
    added_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        has_file = bool(self.file)
        has_link = bool(self.link)

        if has_file == has_link:
            raise ValidationError(
                'A resource must have exactly one of file or link.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name