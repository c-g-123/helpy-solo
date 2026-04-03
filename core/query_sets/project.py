from django.db import models


class ProjectQuerySet(models.QuerySet):

    def for_user(self, user):
        return self.filter(user=user)

    def get_for_user(self, project_id, user):
        return self.for_user(user).get(id=project_id)
