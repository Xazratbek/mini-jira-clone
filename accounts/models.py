from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.urls import reverse


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("account-details", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-id"]
        db_table = "customuser"
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"