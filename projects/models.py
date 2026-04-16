from django.db import models
from accounts.models import CustomUser
from django.urls import reverse
from organization.models import Organization

class Project(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="projects")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_projects")
    members = models.ManyToManyField(CustomUser, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})

    class Meta:
        db_table = "project"
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"
        ordering = ['name']
