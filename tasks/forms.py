from django.forms import ModelForm
from .models import Task
from projects.models import Project
from accounts.models import CustomUser
from organization.models import OrganizationMember

class TaskCreateForm(ModelForm):
    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            self.fields["project"].queryset = Project.objects.filter(
                organization=organization,
                is_active=True,
            ).order_by("name")
            member_ids = OrganizationMember.objects.filter(
                organization=organization,
                is_active=True,
            ).values_list("user_id", flat=True)
            self.fields["assigned_to"].queryset = CustomUser.objects.filter(
                id__in=member_ids
            ).order_by("username")
        else:
            self.fields["project"].queryset = Project.objects.none()
            self.fields["assigned_to"].queryset = CustomUser.objects.none()

    class Meta:
        model = Task
        fields = ["title","description","project","assigned_to","status","priority","due_date"]

class TaskEditForm(ModelForm):
    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization:
            member_ids = OrganizationMember.objects.filter(
                organization=organization,
                is_active=True,
            ).values_list("user_id", flat=True)
            self.fields["assigned_to"].queryset = CustomUser.objects.filter(
                id__in=member_ids
            ).order_by("username")
        else:
            self.fields["assigned_to"].queryset = CustomUser.objects.none()

    class Meta:
        model = Task
        fields = ["title","description","assigned_to","status","priority","due_date"]
