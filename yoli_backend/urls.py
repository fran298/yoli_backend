from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),  # Incluye las rutas de productos
    path('api/services/', include('services.urls')),  # Incluye las rutas de servicios
    path('api/users/', include('users.urls')),  # Incluye las rutas de usuarios (registro)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Ruta para obtener el token (login)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Ruta para refrescar el token
    path('messaging/', include('messaging.urls')),  # Incluye las rutas para la app de mensajes
    path('chatbot/', include('chatbot.urls')),  # Incluye las rutas del chatbot
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)