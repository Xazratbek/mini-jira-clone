from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tasks.models import Task

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/create.html"

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get("task")
        if task_id:
            initial["task"] = get_object_or_404(Task, pk=task_id)
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.task.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = "comments/delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return self.object.task.get_absolute_url()
