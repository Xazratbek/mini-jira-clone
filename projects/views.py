from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ProjectForm
from .models import Project
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q

class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user)).distinct().select_related("owner")

class ProjectDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return super().get_queryset().select_related("owner").prefetch_related("members")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_tasks"] = self.object.tasks.filter(status="IN_PROGRESS").order_by("-created_at")
        context["total_tasks"] = self.object.tasks.count()

        return context

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    template_name = "projects/create.html"
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Project
    template_name = "projects/update.html"
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Project
    template_name = "projects/detail.html"
    success_url = reverse_lazy("project-list")

    def test_func(self):
        obj = self.get_object()

        return obj.owner == self.request.user
