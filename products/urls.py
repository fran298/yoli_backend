from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .views import ProductImageUploadView

router = DefaultRouter()

# Registrar el ProductViewSet con un basename
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/images/', ProductImageUploadView.as_view(), name='product_image_upload'),
]