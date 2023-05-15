from django.urls import path
from studio import views

urlpatterns = [
    path('asset_request/', views.process_asset, name='asset_request'),
    path('library/', views.show_library, name='library'),
]