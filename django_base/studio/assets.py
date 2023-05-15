# STUDIO APP, assets.py
from files_core.models import UploadedFile
from .models import Asset
from .adapters import ProviderOneAdapter, ProviderTwoAdapter
from .utils import get_adapter
from uuid import uuid4
from core.models import AIConfiguration
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests

def create_asset(user, asset_type, prompt, provider, style):
    adapter = get_adapter(provider.name)()
    asset_content = adapter.fetch_asset(asset_type, prompt, style)
    asset_suffix = 'png'
    if asset_content.startswith('http'):
        response = requests.get(asset_content)
        asset_content = response.content
        asset_suffix = response.headers['Content-Type'].split('/')[1]
    safe_prompt = prompt[:20].replace("'", '_').replace('"', '_').replace(' ', '_').replace('.', '_').replace(',', '_').replace('?', '_').replace('!', '_')
    file_name = f'{asset_type}_{user.username}_{uuid4().hex[:8]}_{safe_prompt}'+'.'+asset_suffix
    print(f" file_name is {file_name}")

    clean_file_name = file_name.split("?")[0]
    relative_path = f'assets/{asset_type}/{clean_file_name}'
    default_storage.save(relative_path, ContentFile(asset_content))
    uploaded_file = UploadedFile(file=relative_path)
    uploaded_file.save()
    style_config = AIConfiguration.objects.filter(name=style).first()
    asset = Asset(asset_type=asset_type, prompt=prompt, style=style_config, user=user, file=uploaded_file.file, provider=provider)
    asset.save()
    return asset