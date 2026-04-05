from django.urls import path
from .views import ProjectCreateView, ProjectUpdateView, ProjectDetailView, ProjectDeleteView, ProjectListView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("",cache_page(60)(ProjectListView.as_view()),name="project-list"),
    path("create/",ProjectCreateView.as_view(),name="project-create"),
    path("update/<int:pk>/",ProjectUpdateView.as_view(),name="project-update"),
    path("delete/<int:pk>/",ProjectDeleteView.as_view(),name="project-delete"),
    path("detail/<int:pk>/",ProjectDetailView.as_view(),name="project-detail"),

]
