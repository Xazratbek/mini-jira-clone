from django.conf import settings
from django.core.mail import send_mail

def send_task_deadline_email(task, recipient):
    subject = f"Deadline yaqin: {task.title}"
    message = (
        f"Task: {task.title}\n"
        f"Project: {task.project.name}\n"
        f"Due date: {task.due_date}\n"
        f"Description: {task.description}"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient.email],
        fail_silently=False,
    )