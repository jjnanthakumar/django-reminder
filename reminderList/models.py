import datetime
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

from django.utils import timezone

User = get_user_model()


class Category(models.Model):  # The Category table name that inherits models.Model
    name = models.CharField(max_length=100)  # Like a varchar

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name  # name to be shown when called


# class Status(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name  # name to be shown when called


class TodoList(models.Model):  # Todolist able name that inherits models.Model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)  # a varchar
    content = models.TextField(blank=True)  # a text field
    due_date = models.DateTimeField(default=datetime.datetime.now())  # a date
    category = models.ForeignKey(
        Category, default="general", on_delete=models.PROTECT)  # a foreignkey
    is_active = models.BooleanField(default=True)  # status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # ordering by the created field

    def __str__(self):
        return self.title  # name to be shown when called
