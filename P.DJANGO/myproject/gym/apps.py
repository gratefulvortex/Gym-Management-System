from django.apps import AppConfig
from django.db import models

class GymConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gym'


    class Meta:
        app_label = 'gym'  # Specify the correct app label ('gym' in this case)
