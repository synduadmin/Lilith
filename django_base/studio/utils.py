# studio/utils.py

from .adapters import DallE2Adapter, ProviderTwoAdapter
from core.models import AIConfiguration

def get_adapter(provider_name):
    
    if provider_name == 'Dall-E2':
        return DallE2Adapter
    elif provider_name == 'ProviderTwo':
        return ProviderTwoAdapter
    else:
        raise ValueError('Invalid provider name')
