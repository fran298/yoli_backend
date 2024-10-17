from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ServiceImageUploadView

router = DefaultRouter()

# Registrar el ServiceViewSet con un basename
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),  # Incluir las rutas del router para ServiceViewSet
    path('services/<int:service_id>/images/', ServiceImageUploadView.as_view(), name='service_image_upload'),  # Ruta para cargar imágenes
]