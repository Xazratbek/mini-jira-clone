from django.db import models
from django.urls import reverse
from tasks.models import Task
from accounts.models import CustomUser
from django.urls import reverse

class Comment(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.content[:30]} on task: {self.task.title} | Author: {self.author.username}"

    def get_absolute_url(self):
        return reverse("comment-details", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-id"]
        db_table = "comment"
        verbose_name = "Izox"
        verbose_name_plural = "Izoxlar"