from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

