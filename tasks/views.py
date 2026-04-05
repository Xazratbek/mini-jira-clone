from django.shortcuts import render
from .models import Task
from .forms import TaskCreateForm, TaskEditForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "tasks/create.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user)).select_related("project","assigned_to","created_by")
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priorit=priority)

        assigned_to = self.request.GET.get("assigned_to")
        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)

        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

        return queryset

class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin,DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"

    def test_func(self):
        obj = self.get_object()
        return (obj.created_by == self.request.user) or (obj.assigned_to == self.request.user)

    def get_queryset(self):
        return super().get_queryset().select_related("project","assigned_to","created_by")

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    template_name = "tasks/create.html"
    form_class = TaskCreateForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    template_name = "tasks/update.html"
    form_class = TaskEditForm

    def test_func(self):
        return (self.get_object().created_by == self.request.user) or (self.get_object().assigned_to == self.request.user) or (self.get_object().project.owner == self.request.user)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/update.html"
    success_url = reverse_lazy("task-list")

    def test_func(self):
        return self.get_object().created_by == self.request.user
