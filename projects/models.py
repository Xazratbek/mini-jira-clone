from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.urls import reverse

class Project(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})

    class Meta:
        db_table = "project"
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ['name']