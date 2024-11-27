import os
from django.contrib import messages
import zipfile
from django.conf import settings
from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.urls import reverse

from django.http import HttpResponse


def home(request):
    return redirect(reverse('api_docs'))
    # if request.user.is_authenticated:
    #     return redirect(reverse('api_playground'))
    # else:
    #     return redirect(reverse('account_login'))

def nxtbn_admin(request):
    try:
        return render(request, 'index.html')
    except TemplateDoesNotExist:
        return render(request, 'templatefailback.html')



def upload_admin(request):
    if request.method == 'POST':
        print("POST received with file: ", request.FILES.get('dashboard-upload'))

    if request.method == 'POST' and request.FILES.get('dashboard-upload'):
        uploaded_file = request.FILES['dashboard-upload']
        if not uploaded_file.name.endswith('.zip'):
            messages.error(request, 'Only .zip files are allowed.')
            return redirect('nxtbn_admin')

        # Define paths
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Save the file temporarily
        with open(temp_file_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        try:
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the extracted folder and rename it to 'admin-build'
            extracted_folder = os.path.join(temp_dir, zip_ref.namelist()[0].split('/')[0])
            admin_build_dir = os.path.join(settings.BASE_DIR, 'admin-build')
            if os.path.exists(admin_build_dir):
                os.rmdir(admin_build_dir)
            os.rename(extracted_folder, admin_build_dir)
            
            # Cleanup
            os.remove(temp_file_path)
            messages.success(request, 'File uploaded and extracted successfully.')
            return redirect('nxtbn_admin')
        except zipfile.BadZipFile:
            os.remove(temp_file_path)
            messages.error(request, 'Invalid zip file.')
            return redirect('nxtbn_admin')
        
    return redirect('nxtbn_admin')


