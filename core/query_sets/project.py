from django.db import models


class ProjectQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(user=user)

    def for_parent(self, parent_project, user):
        return self.for_user(user).filter(parent_project=parent_project)

    def top_level(self, user):
        return self.for_user(user).filter(parent_project__isnull=True)
