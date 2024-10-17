import logging
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from .models import Product, ProductImage
from .serializers import ProductImageSerializer
from rest_framework.views import APIView

# Definir un permiso personalizado para los usuarios de tipo 'pyme' o 'emprendedor'
class IsPymeOrEmprendedor(IsAuthenticated):
    def has_permission(self, request, view):
        # Solo los usuarios autenticados con el tipo 'pyme' o 'emprendedor' pueden crear, editar o eliminar
        return super().has_permission(request, view) and request.user.user_type in ['pyme', 'emprendedor']

# Configuramos el logger para la depuración
logger = logging.getLogger('django')

# Vista para los productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Filtrar los productos para que el usuario autenticado solo vea sus propios productos
    def get_queryset(self):
        if self.request.user.is_superuser:
           return Product.objects.all()  # Los superusuarios ven todos los productos
        return Product.objects.filter(user=self.request.user)

    # Asignar permisos según la acción
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            # Solo los usuarios tipo 'pyme' o 'emprendedor' pueden crear, editar o eliminar
            self.permission_classes = [IsPymeOrEmprendedor]
        else:
            # Todos los usuarios autenticados pueden ver los productos
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # Asignar el usuario autenticado como el creador del producto
    def perform_create(self, serializer):
        logger.debug("POST request received: %s", self.request.data)
        print("POST request received:", self.request.data)  # Para depuración
        serializer.save(user=self.request.user)  # Asignar el usuario autenticado al crear un producto

class ProductImageUploadView(APIView):
    """
    Esta vista maneja la subida de imágenes para un producto.
    """
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)  # Obtener el producto al que asociar la imagen
        serializer = ProductImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(product=product)  # Asociar la imagen al producto
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)