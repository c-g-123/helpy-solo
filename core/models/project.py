from django.contrib.auth.models import User
from django.db import models

from core.query_sets.project import ProjectQuerySet


class Project(models.Model):

    MAX_NAME_LENGTH = 30

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_project = models.ForeignKey(
    'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    objects = ProjectQuerySet.as_manager()

    def get_breadcrumbs(self):
        breadcrumbs = []
        current_project = self

        while current_project is not None:
            breadcrumbs.append(current_project)
            current_project = current_project.parent_project

        breadcrumbs.reverse()
        return breadcrumbs

    def __str__(self):
        return self.name
