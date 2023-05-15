import requests
from django.core.files.base import ContentFile
from .models import UploadedFile
import os
from django.conf import settings
from django.contrib.sites.models import Site
from urllib.parse import urljoin
from django.urls import reverse

def download_file( url, file_name):
    print(f"in download file {url}, {file_name}")
    filename = file_name
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = ContentFile(response.content)
    except Exception as e:
        print(f"Error in download_file, unable to obtain request : {e}")

    # Get the current site's domain
    current_site = Site.objects.get_current()
    domain = current_site.domain

    try:
        uploaded_file = UploadedFile(file=filename)
        uploaded_file.file.save(filename, content, save=True)
    except Exception as e:
        print(f"Error in download_file, unable to save file : {e}")

    if settings.ENVIRONMENT == 'production':
        absolute_url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.{settings.AWS_S3_REGION_NAME}.digitaloceanspaces.com/{uploaded_file.file.name}'
    else:
        absolute_url = urljoin(f'http://{domain}', uploaded_file.file.url)

    print(f" uploaded_file.file.url {absolute_url}")
    return absolute_url