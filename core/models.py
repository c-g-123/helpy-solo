from django.contrib.auth.models import User
from django.db import models


_MAX_ITEM_NAME_LENGTH = 50
_MAX_FILENAME_LENGTH = 50
_MAX_DESCRIPTION_LENGTH = 300


class Project(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    # Should colour be a foreign key for a colour table? Otherwise, enums will suffice.

    def __str__(self):
        return self.name


class Task(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    parent_task= models.ForeignKey(
        'self',
           on_delete=models.CASCADE,
           null=True,  # Allow top level tasks to have no parent.
           blank=True,
    )
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    description = models.CharField(
        max_length=_MAX_DESCRIPTION_LENGTH,
        null=True,
        blank=True,
    )
    set_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    # Should status be a foreign key for a status table? Otherwise, enums will suffice.
    # Should priority be a foreign key for a priority table? Otherwise, enums will suffice.

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    # Should colour be a foreign key for a colour table? Otherwise, enums will suffice.
    tags = models.ManyToManyField(User)  # Django will automatically create the link table for this many-to-many relation.


class Resource(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    added_date = models.DateTimeField()
