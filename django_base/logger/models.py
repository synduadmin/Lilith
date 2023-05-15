from django.db import models

# Create your models here.
# create a django model that represent a log record in the database
# the model should have the following fields:
# - id (primary key)
# - timestamp (datetime)
# - level (string)
# - app (string)
# - logger (string)
# - module (string)
# - funcname (string)
# - line_no (integer)
# - message (json)


class LogRecord(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    level = models.CharField(max_length=10)
    app = models.CharField(max_length=255, default="app", null=True, blank=True)
    logger = models.CharField(max_length=255, default="app", null=True, blank=True)
    module = models.CharField(max_length=255, default="app", null=True, blank=True)
    funcname = models.CharField(max_length=255, default="app", null=True, blank=True)
    line_no = models.IntegerField(null=True, blank=True)
    message = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} {self.level} {self.app} {self.logger} {self.module} {self.funcname} {self.line_no} {self.message}"