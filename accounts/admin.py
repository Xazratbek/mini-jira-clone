from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id","username","first_name","last_name","is_staff","created_at"]
    list_filter = ["username","is_staff"]
    search_fields = ["username","first_name","last_name"]