from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# Establece la variable de entorno para el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libro_manager.settings')

app = Celery('libro_manager')

# Configuración usando el sistema de configuración de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubre las tareas en tus apps Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
