# Generated by Django 4.1.7 on 2023-04-24 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import todo_app.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ToDoList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="ToDoItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "due_date",
                    models.DateTimeField(
                        blank=True, default=todo_app.models.one_week_hence, null=True
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("done_comment", models.TextField(blank=True, null=True)),
                (
                    "todo_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="todo_app.todolist",
                    ),
                ),
            ],
            options={
                "ordering": ["due_date"],
            },
        ),
        migrations.CreateModel(
            name="HistoricalToDoList",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=100)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical to do list",
                "verbose_name_plural": "historical to do lists",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalToDoItem",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_date", models.DateTimeField(blank=True, editable=False)),
                (
                    "due_date",
                    models.DateTimeField(
                        blank=True, default=todo_app.models.one_week_hence, null=True
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("done_comment", models.TextField(blank=True, null=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "todo_list",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="todo_app.todolist",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical to do item",
                "verbose_name_plural": "historical to do items",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]