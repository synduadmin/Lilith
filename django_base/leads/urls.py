# leads app, urls.py
from django.urls import path
from .views import HomePageView

app_name = 'leads'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('thank-you/', HomePageView.as_view(template_name='leads/thank_you.html'), name='thank_you'),
]
