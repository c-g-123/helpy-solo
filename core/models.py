from django.contrib.auth.models import User
from django.db import models


_MAX_ITEM_NAME_LENGTH = 50
_MAX_FILENAME_LENGTH = 50
_MAX_DESCRIPTION_LENGTH = 300

class UserSettings(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    DEFAULT_PAGE_CHOICES = [
        ('agenda', 'Agenda'),
        ('calendar', 'Calendar'),
        ('kanban', 'Kanban'),
        ('project', 'Project'),
    ]


    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    default_page = models.CharField(max_length=20, choices=DEFAULT_PAGE_CHOICES, default='agenda')

    def __str__(self):
        return f"{self.user.username}'s settings"
    
    class Meta:
        verbose_name = "User settings"
        verbose_name_plural = "User settings"

class Project(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    # Should colour be a foreign key for a colour table? Otherwise, enums will suffice.

    def __str__(self):
        return self.name


class Task(models.Model):

    #should this be an enum?
    class Status(models.Choices):
        TODO = "ToDo"
        DONE = "Done"
        IN_PROGRESS = "In Progress"

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
    set_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )
    due_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        choices = Status,
        null = True
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

class Tag(models.Model):

    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    # Should colour be a foreign key for a colour table? Otherwise, enums will suffice.
    tags = models.ManyToManyField(User)  # Django will automatically create the link table for this many-to-many relation.


class Resource(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    added_date = models.DateTimeField()
