from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserSettings(models.Model):

    MAX_THEME_LENGTH = 5
    MAX_DEFAULT_BOARD_LENGTH = 8

    class Meta:
        verbose_name = verbose_name_plural = "User settings"

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
    default_board = models.CharField(
        max_length=MAX_DEFAULT_BOARD_LENGTH,
        choices=DefaultBoard.choices,
        default=DefaultBoard.CALENDAR,
    )

    def get_default_board_url(self):
        # return reverse(f"core:{self.default_board.lower()}")
        return reverse('core:agenda')  # TEMPORARY!

    def __str__(self):
        return f"{self.user.username}'s settings"
