import os
from pathlib import Path
from .media import MEDIA_URL, MEDIA_ROOT

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad y configuración de debugging
DEBUG = False  # Cambiado a False para producción y reducir logs
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '1d6e-2a01-11-c10-7860-45b7-1738-f7bc-2062.ngrok-free.app']# Clave secreta (reemplazar en producción con una segura)
SECRET_KEY = 'tu_clave_secreta'

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',  # Habilita CORS
    'rest_framework',
    'rest_framework.authtoken',
    'products',
    'services',
    'users',
    'messaging',
    'chatbot',
]

# Configuración de middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Habilita CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Permite el front-end en desarrollo
    "http://127.0.0.1:3000",  # También localhost con la IP
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-csrftoken',
    'accept',
]

# Configuración de URL y WSGI
ROOT_URLCONF = 'yoli_backend.urls'
WSGI_APPLICATION = 'yoli_backend.wsgi.application'

# Configuración de base de datos (SQLite por defecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos
STATIC_URL = '/static/'

# Directorios adicionales donde Django buscará archivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'static']

# Ruta donde se recopilarán todos los archivos estáticos cuando se ejecute collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Añadir CORS_ORIGIN_ALLOW_ALL si no está permitido
CORS_ORIGIN_ALLOW_ALL = True
# Configuración de autenticación
AUTH_USER_MODEL = 'users.CustomUser'

# Configuración de REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Configuración de TEMPLATES (necesario para usar Django Admin)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Configuración del broker de Celery (Redis)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

MEDIA_URL = '/media/'  # Esta es la URL base para acceder a archivos subidos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Aquí defines la ruta donde se guardarán los archivos en el servidor