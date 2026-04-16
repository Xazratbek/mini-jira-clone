from django import forms
from django.contrib.auth import get_user_model

from .models import Organization, OrganizationMember, RoleChoice

User = get_user_model()


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["name", "description", "website_url", "phone", "email", "logo", "is_active"]


class OrganizationMemberForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Foydalanuvchi",
        empty_label="A'zo tanlang",
    )
    role = forms.ChoiceField(
        choices=[
            (RoleChoice.ADMIN, "Admin"),
            (RoleChoice.MANAGER, "Manager"),
            (RoleChoice.MEMBER, "Member"),
        ],
        label="Rol",
        initial=RoleChoice.MEMBER,
    )

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.organization = organization
        active_member_ids = organization.memberships.filter(is_active=True).values_list("user_id", flat=True)
        self.fields["user"].queryset = (
            User.objects.filter(is_active=True)
            .exclude(id__in=active_member_ids)
            .exclude(id=organization.owner_id)
            .order_by("username")
        )

    def clean_user(self):
        user = self.cleaned_data["user"]
        if self.organization.owner_id == user.id:
            raise forms.ValidationError("Organization owner allaqachon workspace ichida bor.")
        if self.organization.memberships.filter(user=user, is_active=True).exists():
            raise forms.ValidationError("Bu foydalanuvchi organization a'zosi bo'lib turibdi.")
        return user

    def save(self, created_by):
        membership, _ = OrganizationMember.objects.update_or_create(
            organization=self.organization,
            user=self.cleaned_data["user"],
            defaults={
                "role": self.cleaned_data["role"],
                "is_active": True,
                "created_by": created_by,
            },
        )
        return membership
