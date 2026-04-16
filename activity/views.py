from django.shortcuts import render
from .models import ActivityLog
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ActivityFeedView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ActivityLog
    template_name = "feed.html"
    context_object_name = "activities"

    def test_func(self):
        return self.request.user.is_superuser
