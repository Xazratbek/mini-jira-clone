from django.shortcuts import render
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "comments/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = "comments/delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user
