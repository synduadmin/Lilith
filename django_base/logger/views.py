from django.shortcuts import render
from .models import LogRecord
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import LogRecordSerializer

# Create your views here.
# create a viewset that allows log records to be viewed or edited
class LogRecordViewSet(viewsets.ModelViewSet):
    serializer_class = LogRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = LogRecord.objects.all()
