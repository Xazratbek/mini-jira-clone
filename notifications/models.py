from django.db import models
from tasks.models import Task
from accounts.models import CustomUser

class ReminderType(models.TextChoices):
    ONE_DAY = "one_day", "One day before"
    SAME_DAY = "same_day","Same day"
    OVERDUE = "overdue",  "Overdue"

class DeliveryChannel(models.TextChoices):
    EMAIL = "email", "Email"
    TELEGRAM = "telegram", "Telegram"

class DeliveryStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    FAILED = "failed", "Failed"

class TaskReminderLog(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name="reminder_logs")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="task_reminders")
    reminder_type = models.CharField(max_length=20,choices=ReminderType.choices,default=ReminderType.ONE_DAY)
    channel = models.CharField(max_length=20,choices=DeliveryChannel.choices)
    status = models.CharField(max_length=20, choices=DeliveryStatus.choices,default=DeliveryStatus.PENDING)

    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for: {self.task.title} | Status: {self.status} | Error messages: {self.error_message[:50]}"

    class Meta:
        db_table = "task_reminder_log"
        verbose_name = "Vazifa Eslatmasi"
        verbose_name_plural = "Vazifa eslatmasi loglari"
        constraints = [
            models.UniqueConstraint(
                fields=["task","user","reminder_type","channel"],
                name="unique_task_reminder_channel"
            )
        ]
