# leads app, models.py
from django.db import models
from django.conf import settings

class Lead(models.Model):
    INTEREST_CHOICES = [
        ('investor', 'Interested as Investor'),
        ('beta_customer', 'Interested as Beta Customer'),
        ('news', 'Interested as News'),
        ('other', 'Interested as Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    #message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    interested_as = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
