from django.contrib import admin
from .models import TaskReminderLog

@admin.register(TaskReminderLog)
class TaskReminderLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "task",
        "user",
        "reminder_type",
        "channel",
        "status",
        "sent_at",
        "created_at",
    ]
    list_filter = [
        "reminder_type",
        "channel",
        "status",
        "created_at",
        "sent_at",
    ]
    search_fields = [
        "task__title",
        "user__username",
        "user__email",
    ]
    autocomplete_fields = ["task", "user"]
    ordering = ["-created_at"]
