from django.urls import path
from .views import RegisterView, HomeView

urlpatterns = [
    path("signup/",RegisterView.as_view(),name="signup"),
]
