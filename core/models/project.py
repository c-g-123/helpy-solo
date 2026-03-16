from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):

    MAX_NAME_LENGTH = 30

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_NAME_LENGTH)

    def __str__(self):
        return self.name
