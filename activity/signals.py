from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ActivityLog, ActionTypeChoice
from tasks.models import Task
from datetime import date
from comments.models import Comment

@receiver(post_save, sender=Task)
def task_activity_log(sender, instance, created, **kwargs):
    if created:

        action = ActionTypeChoice.CREATED_TASK
        desc = f"Yangi vazifa yaratildi: {instance.title}"
    else:
        action = ActionTypeChoice.UPDATED_TASK
        desc = f"Vazifa tahrirlandi: {instance.title}"

    ActivityLog.objects.create(
        user=instance.created_by,
        action_type=action,
        task=instance,
        description=desc
    )

@receiver(post_save,sender=Comment)
def comment_activity_log(sender,instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(user=instance.author,action_type="commented",task=instance.task,description=f"Comment added to task: {instance.task.title} | Comment: {instance.content[:30]}")