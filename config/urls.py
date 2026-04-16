from django.contrib import admin
from django.urls import path, include
from accounts.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path("tasks/", include("tasks.urls")),
    path("accounts/",include("accounts.urls")),
    path("accounts/",include("django.contrib.auth.urls")),
    path("projects/",include("projects.urls")),
    path("organizations/", include("organization.urls")),
    path("activity/",include("activity.urls")),
    path("comments/",include("comments.urls")),
]
