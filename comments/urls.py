from django.urls import path
from .views import CommentCreateView, CommentDeleteView

urlpatterns = [
    path("create/",CommentCreateView.as_view(),name="comment-create"),
    path("delete/<int:pk>",CommentDeleteView.as_view(),name="comment-delete"),
]
