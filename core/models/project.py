from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from core.query_sets.project import ProjectQuerySet


class Project(models.Model):

    MAX_NAME_LENGTH = 30

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    parent_project = models.ForeignKey(
    'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_projects',
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    objects = ProjectQuerySet.as_manager()

    def clean(self):
        if self.user_id and self.parent_project_id:  # _id fields avoid unnecessary DB queries and crashes.
            if self.user_id != self.parent_project.user_id:
                raise ValidationError('A child project must belong to the same user as its parent project.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

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
