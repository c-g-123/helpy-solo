from django.db import models

from .task import Task


class Resource(models.Model):

    MAX_NAME_LENGTH = 50

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    added_date = models.DateTimeField()
