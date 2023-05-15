from django.urls import path
from .views import HtmlSectionView

app_name = 'html_section'
urlpatterns = [
    path('', HtmlSectionView.as_view(), name="panel_index"),
]
