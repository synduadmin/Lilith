from django.shortcuts import render
from .models import UploadedFile
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'files_core/upload_success.html')
    else:
        form = UploadFileForm()

    return render(request, 'files_core/upload_file.html', {'form': form})
