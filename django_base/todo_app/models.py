# todo_list/todo_app/models.py
from django.utils import timezone
 
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)

class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title

class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence,null=True, blank=True)
    status = models.BooleanField(default=False,blank=False, null=False)
    done_comment = models.TextField(null=True, blank=True)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]