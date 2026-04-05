from django.contrib import admin
from .models import Project

class ProjectMembersInline(admin.TabularInline):
    model = Project.members.through
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMembersInline]
    list_display = ["name","description","owner","created_at","updated_at"]
