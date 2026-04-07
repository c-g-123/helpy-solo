# services/recurrence_service.py

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db import transaction

from ..models.task import Task
from ..models.recurrence_rule import RecurrenceRule


class RecurrenceService:
    """
    Generates and persists recurrence instances for a given RecurrenceRule.

    A recurrence instance is a Task whose recurrence_source is set to the
    base_task of the rule. Instances are generated from the base_task's
    due_datetime, stepping forward by the rule's interval/frequency, and
    stopping at (or before) the rule's end_datetime.
    """

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    @classmethod
    def generate_instances(
        cls,
        rule: RecurrenceRule,
        *,
        from_datetime: datetime | None = None,
        up_to_datetime: datetime | None = None,
    ) -> list[Task]:
        """
        Generate and persist all missing recurrence instances for *rule*.

        Parameters
        ----------
        rule:
            The RecurrenceRule whose instances should be generated.
        from_datetime:
            Only create instances whose due_datetime is >= this value.
            Defaults to the current time, so past instances are skipped.
        up_to_datetime:
            Hard ceiling on instance due_datetime (inclusive). When
            provided it is further constrained by rule.end_datetime.

        Returns
        -------
        list[Task]
            The newly created Task instances (already saved to the DB).

        Raises
        ------
        ValueError
            If base_task has no due_datetime (required as the series origin).
        """
        base_task: Task = rule.base_task

        if base_task.due_datetime is None:
            raise ValueError(
                f"Task pk={base_task.pk} has no due_datetime; "
                "a due_datetime is required to generate recurrence instances."
            )

        effective_from = from_datetime or timezone.now()
        effective_ceiling = cls._effective_ceiling(rule, up_to_datetime)

        # Nothing to generate if there is no ceiling at all (open-ended
        # series without an explicit up_to_datetime) or the ceiling is in
        # the past relative to from_datetime.
        if effective_ceiling is None:
            raise ValueError(
                "Cannot generate instances for an open-ended recurrence rule "
                "without providing an explicit up_to_datetime."
            )

        if effective_ceiling < effective_from:
            return []

        due_datetimes = cls._build_schedule(
            rule=rule,
            origin=base_task.due_datetime,
            from_datetime=effective_from,
            ceiling=effective_ceiling,
        )

        return cls._persist_instances(base_task, due_datetimes)

    # ------------------------------------------------------------------ #
    # Schedule building                                                    #
    # ------------------------------------------------------------------ #

    @classmethod
    def _build_schedule(
        cls,
        rule: RecurrenceRule,
        origin: datetime,
        from_datetime: datetime,
        ceiling: datetime,
    ) -> list[datetime]:
        """
        Return the sorted list of due_datetimes that fall within
        [from_datetime, ceiling] and have not yet been created.
        """
        existing_dates: set[datetime] = cls._existing_instance_dates(rule.base_task)
        delta = cls._delta(rule)

        schedule: list[datetime] = []
        candidate = origin + delta  # first instance is one step ahead of origin

        while candidate <= ceiling:
            if candidate >= from_datetime and candidate not in existing_dates:
                schedule.append(candidate)
            candidate += delta

        return schedule

    @staticmethod
    def _delta(rule: RecurrenceRule):
        """Map a RecurrenceRule to a relativedelta step."""
        freq = rule.frequency
        n = rule.interval

        if freq == RecurrenceRule.Frequency.DAILY:
            return relativedelta(days=n)
        if freq == RecurrenceRule.Frequency.WEEKLY:
            return relativedelta(weeks=n)
        if freq == RecurrenceRule.Frequency.MONTHLY:
            return relativedelta(months=n)

        raise ValueError(f"Unsupported frequency: {freq!r}")

    # ------------------------------------------------------------------ #
    # Persistence                                                          #
    # ------------------------------------------------------------------ #

    @classmethod
    @transaction.atomic
    def _persist_instances(
        cls,
        base_task: Task,
        due_datetimes: list[datetime],
    ) -> list[Task]:
        """Bulk-create Task instances for every due_datetime in the list."""
        if not due_datetimes:
            return []

        instances = [
            Task(
                user=base_task.user,
                project=base_task.project,
                parent_task=base_task.parent_task,
                recurrence_source=base_task,
                name=base_task.name,
                description=base_task.description,
                due_datetime=due_dt,
                # Each instance starts fresh as TO_DO regardless of the
                # base task's current status.
                status=Task.Status.TO_DO,
            )
            for due_dt in due_datetimes
        ]

        # bulk_create bypasses Model.save / full_clean, so we validate
        # every instance explicitly before committing.
        for instance in instances:
            instance.full_clean()

        return Task.objects.bulk_create(instances)

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _effective_ceiling(
        rule: RecurrenceRule,
        up_to_datetime: datetime | None,
    ) -> datetime | None:
        """
        The tightest upper bound: the minimum of rule.end_datetime and
        up_to_datetime (either may be None).
        """
        candidates = [dt for dt in (rule.end_datetime, up_to_datetime) if dt is not None]
        return min(candidates) if candidates else None

    @staticmethod
    def _existing_instance_dates(base_task: Task) -> set[datetime]:
        """Return the set of due_datetimes already generated for base_task."""
        return set(
            base_task.instances
            .exclude(due_datetime=None)
            .values_list("due_datetime", flat=True)
        )
