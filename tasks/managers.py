from django.db import models
from datetime import date

class TaskManager(models.Manager):
    def active(self):
        return self.filter(status="in_progress")

    def by_user(self, user):
        return self.filter(created_by=user)

    def by_project(self, project_id):
        return self.filter(project__id=project_id)

    def overdue(self, date):
        today = date.today()
        return self.filter(due_date__lt=today)