# Django project's urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gym.urls')),  # Include your app's URLs
]
