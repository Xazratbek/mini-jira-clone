from django.contrib import admin
from .models import Organization, OrganizationMember

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id","name","owner","is_active"]
    list_filter = ["is_active","created_at"]
    search_fields = ["name","owner__username","phone","email"]

    prepopulated_fields = {"slug": ("name",)}

@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ["organization","user","role","is_active"]
    list_filter = ["organization","is_active","joined_at","role"]
    search_fields = ["organization__name","user__username"]
