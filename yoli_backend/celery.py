from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer el entorno de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yoli_backend.settings')

# Crear una nueva instancia de Celery
app = Celery('yoli_backend')

# Cargar la configuración desde Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir tareas de todos los archivos tasks.py en las aplicaciones
app.autodiscover_tasks()