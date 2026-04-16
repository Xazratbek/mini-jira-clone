from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from .forms import OrganizationForm, OrganizationMemberForm
from .models import Organization, OrganizationMember, RoleChoice, get_user_organization


class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = "organization/list.html"
    context_object_name = "organizations"

    def get_queryset(self):
        return (
            Organization.objects.filter(
                Q(owner=self.request.user) | Q(memberships__user=self.request.user, memberships__is_active=True)
            )
            .distinct()
            .select_related("owner")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manageable_org_ids"] = {
            organization.id for organization in context["organizations"] if organization.can_manage(self.request.user)
        }
        return context


class OrganizationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Organization
    template_name = "organization/detail.html"
    context_object_name = "organization"

    def get_queryset(self):
        return super().get_queryset().select_related("owner").prefetch_related("memberships__user", "projects")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_count"] = self.object.memberships.filter(is_active=True).count()
        context["project_count"] = self.object.projects.count()
        context["active_tasks_count"] = sum(
            project.tasks.exclude(status="done").count()
            for project in self.object.projects.all()
        )
        context["can_manage_organization"] = self.object.can_manage(self.request.user)
        return context

    def test_func(self):
        organization = self.get_object()
        return organization.is_member(self.request.user)


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = "organization/create.html"
    form_class = OrganizationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        OrganizationMember.objects.get_or_create(
            organization=self.object,
            user=self.request.user,
            defaults={
                "role": RoleChoice.OWNER,
                "is_active": True,
                "created_by": self.request.user,
            },
        )
        return response

    def get_success_url(self):
        return self.object.get_absolute_url()


class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    template_name = "organization/update.html"
    form_class = OrganizationForm

    def test_func(self):
        organization = self.get_object()
        return organization.can_manage(self.request.user)

    def get_success_url(self):
        return self.object.get_absolute_url()


class OrganizationMemberAddView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "organization/member_add.html"
    form_class = OrganizationMemberForm

    def dispatch(self, request, *args, **kwargs):
        self.organization = get_object_or_404(Organization.objects.select_related("owner"), pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["organization"] = self.organization
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization"] = self.organization
        return context

    def form_valid(self, form):
        membership = form.save(created_by=self.request.user)
        display_name = membership.user.get_full_name() or membership.user.username
        messages.success(self.request, f"{display_name} organizationga qo'shildi.")
        return redirect(self.organization.get_absolute_url())

    def test_func(self):
        return self.organization.can_manage(self.request.user)
