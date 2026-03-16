from django.contrib.auth.models import User
from django.db import models

from .task import Task


class Tag(models.Model):

    MAX_NAME_LENGTH = 20

    name = models.CharField(max_length=MAX_NAME_LENGTH)
    user_tags = models.ManyToManyField(User)  # Django will automatically create the link table for this many-to-many relation.
    task_tags = models.ManyToManyField(Task)
