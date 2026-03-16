from django.contrib.auth.models import User
from django.db import models


class UserSettings(models.Model):

    MAX_THEME_LENGTH = 5
    MAX_DEFAULT_BOARD_LENGTH = 8

    class Theme(models.TextChoices):
        LIGHT = 'LIGHT', 'Light'
        DARK = 'DARK', 'Dark'

    class DefaultBoard(models.TextChoices):
        AGENDA = 'AGENDA', 'Agenda'
        CALENDAR = 'CALENDAR', 'Calendar'
        KANBAN = 'KANBAN', 'Kanban'
        PROJECT = 'PROJECT', 'Project'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(
        max_length=MAX_THEME_LENGTH,
        choices=Theme.choices,
        default=Theme.LIGHT,
    )
    default_page = models.CharField(
        max_length=MAX_DEFAULT_BOARD_LENGTH,
        choices=DefaultBoard.choices,
        default=DefaultBoard.CALENDAR,
    )

    def __str__(self):
        return f"{self.user.username}'s settings"

    class Meta:
        verbose_name = verbose_name_plural = "User settings"
