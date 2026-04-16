from django.urls import path

from .views import (
    OrganizationCreateView,
    OrganizationDetailView,
    OrganizationListView,
    OrganizationMemberAddView,
    OrganizationUpdateView,
)


urlpatterns = [
    path("", OrganizationListView.as_view(), name="organization-list"),
    path("create/", OrganizationCreateView.as_view(), name="organization-create"),
    path("detail/<int:pk>/", OrganizationDetailView.as_view(), name="organization-detail"),
    path("detail/<int:pk>/members/add/", OrganizationMemberAddView.as_view(), name="organization-member-add"),
    path("update/<int:pk>/", OrganizationUpdateView.as_view(), name="organization-update"),
]
