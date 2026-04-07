from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from .project import Project
from core.query_sets.task import TaskQuerySet


class Task(models.Model):

    MAX_NAME_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 300
    MAX_STATUS_LENGTH = 11

    class Status(models.TextChoices):

        TO_DO = 'TO_DO', 'To-do'
        IN_PROGRESS = "IN_PROGRESS", "In-progress"
        DONE = 'DONE', 'Done'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks',
    )
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_tasks',
    )
    recurrence_source = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='instances'
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.TextField(
        null=True,
        blank=True,
    )
    due_datetime = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=MAX_STATUS_LENGTH,
        choices=Status.choices,
        default=Status.TO_DO,
    )
    objects = TaskQuerySet.as_manager()

    def clean(self):
        if not self.user_id:  # _id fields avoid unnecessary DB queries and crashes.
            raise ValidationError('A task must have an associated user.')

        if self.project_id:
            if self.user_id != self.project.user_id:
                raise ValidationError('A task must have the same user as its parent project.')

        if self.parent_task_id:
            if self.user_id != self.parent_task.user_id:
                raise ValidationError('A child task must have the same user as its parent task.')
            if self.project_id != self.parent_task.project_id:
                raise ValidationError('A child task must have the same project as its parent task.')

        if self.recurrence_source_id:
            if self.user_id != self.recurrence_source.user_id:
                raise ValidationError('A task must have the same user as its recurrence source.')
            if self.project_id != self.recurrence_source.project_id:
                raise ValidationError('A task must have the same project as its recurrence source.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_breadcrumbs(self):
        breadcrumbs = []
        current_task = self

        while current_task.parent_task:
            breadcrumbs.append(current_task)
            current_task = current_task.parent_task

        current_project = current_task.project
        while current_project:
            breadcrumbs.append(current_project)
            current_project = current_project.parent_project

        breadcrumbs.reverse()
        return breadcrumbs

    def __str__(self):
        return self.name
