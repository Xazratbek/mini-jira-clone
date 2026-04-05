from django.db import models
from accounts.models import CustomUser
from tasks.models import Task

class ActionTypeChoice(models.TextChoices):
    CREATED_TASK = "created_task", "Created task"
    UPDATED_TASK = "updated_task","Updated task"
    DELETED_TASK = "deleted_task","Deleted task"
    COMMENTED = "commented","Commented"


class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,related_name="activity_logs")
    action_type = models.CharField(max_length=50,choices=ActionTypeChoice.choices)
    task = models.ForeignKey(Task,on_delete=models.SET_NULL,related_name="activity_logs",null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log on task: {self.task.title} | User: {self.user.get_full_name()} | Desc: {self.description[:30]}... | Action type: {self.action_type}"

    class Meta:
        db_table = "activity_log"
        verbose_name = "Faoliyat jurnali"
        verbose_name_plural = "Faoliyat jurnallari"