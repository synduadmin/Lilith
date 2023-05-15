# studio/views.py
import requests
import os
from django.shortcuts import render
from django.conf import settings
from .forms import AssetRequestForm
from .models import Asset
from files_core.models import UploadedFile
from .adapters import ProviderOneAdapter, ProviderTwoAdapter  # Import the adapters
from .utils import get_adapter
from uuid import uuid4
from core.models import AIConfiguration
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .assets import create_asset  # Import the create_asset function


@login_required
def process_asset(request):
    if request.method == 'POST':
        print("in process_asset")
        form = AssetRequestForm(request.POST)
        if form.is_valid():
            asset_type = form.cleaned_data['asset_type']
            prompt = form.cleaned_data['prompt']
            user = form.cleaned_data['user']
            provider = form.cleaned_data['provider']
            style = form.cleaned_data['style']
            print(f"asset_type : {asset_type}, prompt : {prompt}, user : {user}, provider : {provider}")
            # Call the create_asset function
            asset = create_asset(user, asset_type, prompt, provider, style)
            return render(request, 'studio/asset_result.html', {'asset': asset})
    else:
        form = AssetRequestForm()
    return render(request, 'studio/asset_request.html', {'form': form})

@login_required
def show_library(request):
    assets = Asset.objects.all()
    return render(request, 'studio/library.html', {'assets': assets})

