from django.db import models


class TaskQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(project__user=user)

    def for_parent(self, task, user):
        return self.filter(parent_task=task, project__user=user)

    def top_level(self, user):
        return self.filter(parent_task__isnull=True, project__user=user)

    def top_level_to_do(self, user):
        return self.filter(parent_task__isnull=True, status=self.model.Status.TO_DO, project__user=user)

    def top_level_in_progress(self, user):
        return self.filter(parent_task__isnull=True, status=self.model.Status.IN_PROGRESS, project__user=user)

    def top_level_done(self, user):
        return self.filter(parent_task__isnull=True, status=self.model.Status.DONE, project__user=user)

    def active_top_level_for_project(self, project_id, user):
        return self.filter(
            project_id=project_id,
            parent_task__isnull=True,
            project__user=user,
            status__in=[self.model.Status.TO_DO, self.model.Status.IN_PROGRESS],
        )
