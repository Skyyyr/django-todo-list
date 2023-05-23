from django.db import models
from datetime import datetime

from django.urls import reverse


class ToDoList(models.Model):
    name = models.CharField(max_length=256, null=False)

    def __str__(self):
        return f"{self.name}"


class ToDo(models.Model):
    name = models.CharField(max_length=256, null=False)
    created_at = models.TimeField(default=datetime.time(datetime.now()), null=False)
    completed_at = models.TimeField(null=True, blank=True)
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
