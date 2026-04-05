from django.db import models


class TaskQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(project__user=user)

    def for_parent(self, parent_task, user):
        return self.for_user(user).filter(parent_task=parent_task)

    def for_project(self, project, user):
        return self.for_user(user).filter(project=project)

    def top_level(self, user):
        return self.for_user(user).filter(parent_task__isnull=True)
