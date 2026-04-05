from django.forms import ModelForm
from .models import Task

class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class TaskEditForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title","description","assigned_to","status","priority","due_date"]
