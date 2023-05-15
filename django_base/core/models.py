from django.db import models
from django.conf import settings 
import uuid
from simple_history.models import HistoricalRecords

# Create your models here.
class AIConfiguration(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    prime = models.TextField(null=True, blank=True)
    model = models.CharField(max_length=200, null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    max_tokens = models.IntegerField(null=True, blank=True)
    top_p = models.FloatField(null=True, blank=True)
    top_k = models.IntegerField(null=True, blank=True)
    frequency_penalty = models.FloatField(null=True, blank=True)
    presence_penalty = models.FloatField(null=True, blank=True)
    stop = models.CharField(max_length=200, null=True, blank=True)
    default_depth = models.IntegerField(null=True, blank=True)
    api_key = models.CharField(max_length=200, null=True, blank=True)
    org_id = models.CharField(max_length=200, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class AIInteraction(models.Model):
    id = models.AutoField(primary_key=True)
    configuration_id = models.ForeignKey(AIConfiguration, on_delete= models.CASCADE, related_name='configuration_id', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    input = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='interacting_user', null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    output = models.TextField()
    json = models.JSONField(null=True, blank=True)
    blob = models.BinaryField(null=True, blank=True)
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.id)
