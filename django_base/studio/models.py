# studio/models.py
from django.contrib.auth.models import User
from django.db import models
from core.models import AIConfiguration

class AssetProvider(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define primary key field
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Asset(models.Model):
    ASSET_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('ppt', 'PPT'),
        ('pdf', 'PDF'),
        # Add more asset types here
    ]

    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    prompt = models.TextField()
    style = models.ForeignKey(AIConfiguration, 
                              on_delete=models.DO_NOTHING,
                              limit_choices_to={'model': 'image-alpha-001'})
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assets/')
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    provider = models.ForeignKey(AssetProvider, on_delete=models.CASCADE)

    
# Add your DallE2 adapter here
dalle_2 = AssetProvider.objects.get_or_create(name='Dall-E2')[0]

