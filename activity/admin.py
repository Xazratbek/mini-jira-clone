from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user__username","action_type","task__title","created_at"]
    list_filter =  ["user__username","action_type"]
