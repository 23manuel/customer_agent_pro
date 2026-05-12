from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect # Import this

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/', include('api.urls')),
    # Add this line to redirect the empty path to your dashboard
    path('', lambda request: redirect('api/dashboard/', permanent=False)),
]