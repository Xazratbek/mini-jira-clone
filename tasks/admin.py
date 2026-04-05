from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id","title","project","assigned_to","created_by","status","priority","due_date"]
    list_filter = ["project","status","priority","due_date"]
    search_fields = ["title","project"]
