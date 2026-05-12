# novapay_backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Change 'local_admin_url' to 'urls'
    path('admin/', admin.site.urls), 
    
    path('api/', include('api.urls')),
]