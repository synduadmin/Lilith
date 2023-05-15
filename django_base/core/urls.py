from django.urls import path
from . import views

urlpatterns = [
    path('ai-interaction/', views.ai_interaction, name='ai-interaction'),
]
