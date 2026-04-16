from django.forms import ModelForm
from .models import Project
from organization.models import OrganizationMember

class ProjectForm(ModelForm):
    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.organization = organization
        if organization:
            self.fields["members"].queryset = (
                OrganizationMember.objects.filter(organization=organization, is_active=True)
                .select_related("user")
                .values_list("user", flat=True)
            )
            from accounts.models import CustomUser
            self.fields["members"].queryset = CustomUser.objects.filter(
                id__in=self.fields["members"].queryset
            ).order_by("username")
        else:
            self.fields["members"].queryset = self.fields["members"].queryset.none()

    class Meta:
        model = Project
        fields = ["name","description","members"]
