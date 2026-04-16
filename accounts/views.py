from django.shortcuts import render
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from .models import CustomUser
from tasks.models import Task
from projects.models import Project
from django.db.models import Q
from organization.models import get_user_organization

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class HomeView(TemplateView):
    template_name = "landing_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            organization = get_user_organization(user)
            my_projects = Project.objects.filter(
                organization=organization,
            ).filter(
                Q(owner=user) | Q(members=user) | Q(organization__owner=user),
                is_active=True,
            ).distinct()
            my_tasks = Task.objects.filter(
                project__organization=organization,
            ).filter(
                Q(created_by=user) | Q(assigned_to=user)
            ).distinct()

            context["active_projects"] = my_projects.count()
            context["tugagan_vazifalar"] = my_tasks.filter(status="done").count()
            context["open_tasks"] = my_tasks.exclude(status="done").count()
            context["assigned_tasks"] = my_tasks.filter(assigned_to=user).count()
            context["organization_name"] = organization.name if organization else None
        else:
            context["active_users"] = CustomUser.objects.filter(is_active=True).count()
            context["tugagan_vazifalar"] = Task.objects.filter(status="done").count()
            context["active_projects"] = Project.objects.filter(is_active=True).count()
        return context
