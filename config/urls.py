from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("tasks.urls")),
    path("accounts/",include("accounts.urls")),
    path("accounts/",include("django.contrib.auth.urls")),
    path("projects/",include("projects.urls")),
    path("activity/",include("activity.urls")),
    path("comments/",include("comments.urls")),
]
