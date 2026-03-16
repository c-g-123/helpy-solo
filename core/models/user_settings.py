from django.contrib.auth.models import User
from django.db import models


class UserSettings(models.Model):

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(choices=THEME_CHOICES, default='light')
    default_page = models.CharField(choices=DEFAULT_PAGE_CHOICES, default='agenda')

    def __str__(self):
        return f"{self.user.username}'s settings"

    class Meta:
        verbose_name = verbose_name_plural = "User settings"
