from django.db import models

from .task import Task


class RecurrenceRule(models.Model):

    MAX_FREQUENCY_LENGTH = 7
    DEFAULT_INTERVAL = 1

    class Frequency(models.TextChoices):

        DAILY   = 'DAILY',   'Daily'
        WEEKLY  = 'WEEKLY',  'Weekly'
        MONTHLY = 'MONTHLY', 'Monthly'

    base_task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name='recurrence_rule',
    )
    interval         = models.PositiveIntegerField(default=DEFAULT_INTERVAL)
    frequency        = models.CharField(max_length=MAX_FREQUENCY_LENGTH, choices=Frequency.choices)
    end_datetime     = models.DateTimeField(null=True, blank=True)
