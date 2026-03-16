from django.db import models

from core.models.project import Project


class Task(models.Model):

    MAX_NAME_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 300

    # should this be an enum?
    class Status(models.TextChoices):
        TODO = "ToDo"
        DONE = "Done"
        IN_PROGRESS = "In Progress"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,  # Allow top level tasks to have no parent.
        blank=True,
    )
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.CharField(
        max_length=MAX_DESCRIPTION_LENGTH,
        null=True,
        blank=True,
    )
    set_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )
    due_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        choices=Status.choices,
        null=True
    )

    # Should status be a foreign key for a status table? Otherwise, enums will suffice.
    # Should priority be a foreign key for a priority table? Otherwise, enums will suffice.

    def __str__(self):
        return self.name

    def get_breadcrumbs(self):
        breadcrumbs = []
        current_task = self

        while current_task is not None:
            breadcrumbs.append(current_task)
            current_task = current_task.parent_task

        breadcrumbs.reverse()
        return breadcrumbs
