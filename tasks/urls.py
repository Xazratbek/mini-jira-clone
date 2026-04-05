from django.urls import path
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView, TaskDetailView, TaskListView

urlpatterns = [
    path("",TaskListView.as_view(),name="task-list"),
    path("update/<int:pk>",TaskUpdateView.as_view(),name="task-update"),
    path("delete/<int:pk>/",TaskDeleteView.as_view(),name="task-delete"),
    path("detail/<int:pk>/",TaskDetailView.as_view(),name="task-detail"),
    path("create/",TaskCreateView.as_view(),name="task-create"),
]
