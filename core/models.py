from django.contrib.auth.models import User
from django.db import models


_MAX_ITEM_NAME_LENGTH = 50
_MAX_FILENAME_LENGTH = 50
_MAX_DESCRIPTION_LENGTH = 300


# Uncomment this if we decide to add more fields to the user model than django.contrib.auth provides.
# class UserProfile(models.Model):
#
#     # This line is required. Links UserProfile to a User model instance.
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Import from django.contrib.auth.
#
#     # The additional attributes we wish to include...
#
#     def __str__(self):
#         return self.user.username


class Project(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    # Should colour be a foreign key for a colour table? Otherwise, enums will suffice.

    def __str__(self):
        return self.name


class Task(models.Model):

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    description = models.CharField(max_length=_MAX_DESCRIPTION_LENGTH)
    set_date = models.DateTimeField()
    due_date = models.DateTimeField()
    # Should status be a foreign key for a status table? Otherwise, enums will suffice.
    # Should priority be a foreign key for a priority table? Otherwise, enums will suffice.


class Tag(models.Model):

    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    # Should colour be a foreign key for a colour table? Otherwise, enums will suffice.
    tags = models.ManyToManyField(User)  # Django will automatically create the link table for this many-to-many relation.


class Resource(models.Model):

    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=_MAX_ITEM_NAME_LENGTH)
    added_date = models.DateTimeField()
