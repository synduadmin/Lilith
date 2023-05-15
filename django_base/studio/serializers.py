# studio/serializers.py
from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['asset_type', 'prompt', 'user','style', 'file']
