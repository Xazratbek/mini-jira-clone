from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from .models import TaskReminderLog, ReminderType, DeliveryChannel, DeliveryStatus
from .services import send_task_deadline_email
from django.db import IntegrityError, transaction

@shared_task
def check_deadline_reminders():
    tomorrow = timezone.localdate() + timedelta(days=1)

    tasks = Task.objects.filter(
        due_date=tomorrow,
        assigned_to__isnull=False,
    ).select_related("assigned_to", "project")

    for task in tasks:
        if not task.assigned_to.email or not task.assigned_to:
            continue

        already_sent = TaskReminderLog.objects.filter(
            task=task,
            user=task.assigned_to,
            reminder_type=ReminderType.ONE_DAY,
            channel=DeliveryChannel.EMAIL,
            status=DeliveryStatus.SENT,
        ).exists()

        try:
            with transaction.atomic():
                TaskReminderLog.objects.create(
                    task=task,
                    user=task.assigned_to,
                    reminder_type=ReminderType.ONE_DAY,
                    channel=DeliveryChannel.EMAIL,
                    status=DeliveryStatus.PENDING
                )
        except IntegrityError:
            continue

        send_deadline_email_task.delay(task.id)

@shared_task
def send_deadline_email_task(task_id):
    task = Task.objects.select_related("assigned_to", "project").get(id=task_id)

    if not task.assigned_to or not task.assigned_to.email:
        return "Qabul qiluvchi mavjud emas"

    log = TaskReminderLog.objects.get(
        task=task,
        user=task.assigned_to,
        reminder_type=ReminderType.ONE_DAY,
        channel=DeliveryChannel.EMAIL,
        defaults={"status": DeliveryStatus.PENDING},
    )

    if log.status == DeliveryStatus.SENT:
        return "already sent"

    try:
        send_task_deadline_email(task, task.assigned_to)
        log.status = DeliveryStatus.SENT
        log.sent_at = timezone.now()
        log.error_message = ""
        log.save(update_fields=["status", "sent_at", "error_message"])
        return "yuborildi"

    except Exception as exc:
        log.status = DeliveryStatus.FAILED
        log.error_message = str(exc)
        log.save(update_fields=["status", "error_message"])
        raise
