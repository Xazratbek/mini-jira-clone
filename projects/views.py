from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ProjectForm
from .models import Project
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from organization.models import RoleChoice, get_user_organization

class ProjectListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = "projects/list.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        organization = get_user_organization(self.request.user)
        if not organization:
            return Project.objects.none()
        return (
            Project.objects.filter(
                organization=organization
            )
            .filter(
                Q(owner=self.request.user)
                | Q(members=self.request.user)
                | Q(organization__owner=self.request.user)
                | Q(
                    organization__memberships__user=self.request.user,
                    organization__memberships__role__in=[
                        RoleChoice.ADMIN,
                        RoleChoice.MANAGER,
                        RoleChoice.OWNER,
                    ],
                )
            )
            .distinct()
            .select_related("owner", "organization")
            .prefetch_related("members")
        )

class ProjectDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Project
    template_name = "projects/detail.html"
    context_object_name = "project"

    def get_queryset(self):
        organization = get_user_organization(self.request.user)
        queryset = super().get_queryset().select_related("owner", "organization").prefetch_related("members")
        if not organization:
            return queryset.none()
        return queryset.filter(organization=organization)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_tasks"] = self.object.tasks.filter(status__in=["todo","in_progress"]).order_by("-created_at")

        return context

    def test_func(self):
        obj = self.get_object()
        return (
            obj.owner == self.request.user
            or obj.members.filter(pk=self.request.user.pk).exists()
            or obj.organization.can_manage(self.request.user)
        )

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    template_name = "projects/create.html"
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = get_user_organization(self.request.user)
        return kwargs

    def form_valid(self, form):
        organization = get_user_organization(self.request.user)
        if not organization:
            form.add_error(None, "Avval organization yaratilishi yoki organizationga a'zo bo'lishingiz kerak.")
            return self.form_invalid(form)
        form.instance.organization = organization
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Project
    template_name = "projects/update.html"
    form_class = ProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = self.get_object().organization
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.get_object().owner
        form.instance.organization = self.get_object().organization
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or obj.organization.can_manage(self.request.user)

class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Project
    template_name = "projects/detail.html"
    success_url = reverse_lazy("project-list")

    def test_func(self):
        obj = self.get_object()

        return obj.owner == self.request.user or obj.organization.can_manage(self.request.user)
