from django.db import models
from projects.models import Project
from accounts.models import CustomUser
from django.urls import reverse
from .managers import TaskManager

class TaskStatusChoice(models.TextChoices):
    TODO = "todo", "Todo"
    IN_PROGRESS = "in_progress", "In Progress"
    DONE = "done", "Done"


class TaskPriorityChoice(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"

class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name="tasks")
    assigned_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="assigned_tasks")
    created_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,related_name="tasks")
    status = models.CharField(max_length=35,choices=TaskStatusChoice.choices,default=TaskStatusChoice.TODO)
    priority = models.CharField(max_length=25,choices=TaskPriorityChoice.choices,default=TaskPriorityChoice.LOW)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskManager()


    def __str__(self):
        return f"Task: {self.title} | Created by: {self.created_by} | Assigned to: {self.assigned_to}"

    def get_absolute_url(self):
        return reverse("task-detail", kwargs={"pk": self.pk})

    class Meta:
        db_table = "task"
        ordering = ["title"]
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
