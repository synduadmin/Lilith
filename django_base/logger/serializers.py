#serializer for log record
from rest_framework import serializers
from .models import LogRecord

class LogRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogRecord
        fields = '__all__'
        