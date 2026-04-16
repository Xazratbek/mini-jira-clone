from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import CustomUser
from organization.models import Organization, OrganizationMember, RoleChoice
from django.db import transaction

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    organization_name = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "organization_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu emailni boshqa foydalanuvchi allaqachon ishlatayapti.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            organization = Organization.objects.create(
                name=self.cleaned_data["organization_name"],
                owner=user,
            )
            OrganizationMember.objects.create(
                organization=organization,
                user=user,
                role=RoleChoice.OWNER,
                created_by=user,
            )
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ["first_name","last_name"]
