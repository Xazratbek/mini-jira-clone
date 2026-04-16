from django.shortcuts import render
from .models import Task
from .forms import TaskCreateForm, TaskEditForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from organization.models import RoleChoice, get_user_organization
from django.core.cache import cache

class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        organization = get_user_organization(self.request.user)
        if not organization:
            return Task.objects.none()

        query_string = self.request.GET.urlencode()
        cache_key = f"task_list_user_{self.request.user.id}_org_{organization.id}_{query_string}"

        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset

        queryset = Task.objects.filter(
            project__organization=organization
        ).filter(
            Q(created_by=self.request.user)
            | Q(assigned_to=self.request.user)
            | Q(project__owner=self.request.user)
            | Q(project__organization__owner=self.request.user)
            | Q(
                project__organization__memberships__user=self.request.user,
                project__organization__memberships__role__in=[
                    RoleChoice.ADMIN,
                    RoleChoice.MANAGER,
                    RoleChoice.OWNER,
                ],
            )
        ).distinct().select_related("project","assigned_to","created_by", "project__organization")

        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        assigned_to = self.request.GET.get("assigned_to")
        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

        cache.set(cache_key,queryset,60*10)

        return queryset

class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin,DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"

    def test_func(self):
        obj = self.get_object()
        return (
            obj.created_by == self.request.user
            or obj.assigned_to == self.request.user
            or obj.project.owner == self.request.user
            or obj.project.organization.can_manage(self.request.user)
        )

    def get_queryset(self):
        organization = get_user_organization(self.request.user)
        queryset = super().get_queryset().select_related("project","assigned_to","created_by", "project__organization")
        if not organization:
            return queryset.none()
        return queryset.filter(project__organization=organization)

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    template_name = "tasks/create.html"
    form_class = TaskCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = get_user_organization(self.request.user)
        return kwargs

    def form_valid(self, form):
        organization = get_user_organization(self.request.user)
        if not organization:
            form.add_error(None, "Task yaratish uchun organizationga tegishli bo'lishingiz kerak.")
            return self.form_invalid(form)
        if form.cleaned_data["project"].organization_id != organization.id:
            form.add_error("project", "Faqat o'zingizning organization loyihasiga task qo'sha olasiz.")
            return self.form_invalid(form)
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = "tasks/update.html"
    form_class = TaskEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = self.get_object().project.organization
        return kwargs

    def test_func(self):
        obj = self.get_object()
        return (
            obj.created_by == self.request.user
            or obj.assigned_to == self.request.user
            or obj.project.owner == self.request.user
            or obj.project.organization.can_manage(self.request.user)
        )

    def form_valid(self, form):
        form.instance.created_by = self.get_object().created_by
        form.instance.project = self.get_object().project
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/update.html"
    success_url = reverse_lazy("task-list")

    def test_func(self):
        obj = self.get_object()
        return obj.created_by == self.request.user or obj.project.organization.can_manage(self.request.user)
