# studio/adapters.py
import requests
import base64
import os
from django.conf import settings
from abc import ABC, abstractmethod
from core.views import openai_wrapper, dalle_wrapper
from core.models import AIConfiguration

class AssetAdapter(ABC):

    @abstractmethod
    def fetch_asset(self, asset_type, prompt):
        pass

class DallE2Adapter(AssetAdapter):
    def fetch_asset(self, asset_type, prompt, style):
        print(f"asset_type : {asset_type}, prompt : {prompt}")
        try:
            print(f"in DallE2Adapter {prompt}")
            image_url = dalle_wrapper(prompt, style)
            return image_url
        
        except Exception as e:
            print(f"Error in DallE2 Adapter : {e}")
            return ''

class ProviderOneAdapter(AssetAdapter):

    BASE_URL = 'https://provider_one.example.com/assets/'

    def fetch_asset(self, asset_type, prompt, style):
        response = requests.post(f'{self.BASE_URL}{asset_type}', data={'prompt': prompt})

        if response.status_code == 200:
            return response.content
        else:
            raise Exception('Error fetching asset from ProviderOne')

class ProviderTwoAdapter(AssetAdapter):

    BASE_URL = 'https://provider_two.example.com/assets/'

    def fetch_asset(self, asset_type, prompt, style):
        response = requests.post(f'{self.BASE_URL}{asset_type}', data={'prompt': prompt})

        if response.status_code == 200:
            return response.content
        else:
            raise Exception('Error fetching asset from ProviderTwo')

# Add more adapters for other providers as needed
