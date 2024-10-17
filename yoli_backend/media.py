import os
from pathlib import Path

# BASE_DIR es necesario para determinar la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Definir la ruta para guardar archivos subidos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')