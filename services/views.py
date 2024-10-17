from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Service, ServiceImage
from .serializers import ServiceSerializer, ServiceImageSerializer


# Permiso personalizado para 'pyme' o 'emprendedor'
class IsPymeOrEmprendedor(IsAuthenticated):
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y sea 'pyme' o 'emprendedor'
        return super().has_permission(request, view) and request.user.user_type in ['pyme', 'emprendedor']


# Vista para los servicios
class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        # Filtra los servicios del usuario autenticado
        return Service.objects.filter(user=self.request.user)

    def get_permissions(self):
        # Define permisos dependiendo de la acción
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsPymeOrEmprendedor]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Asigna el usuario autenticado al servicio creado
        serializer.save(user=self.request.user)


# Vista para subir imágenes de servicios
class ServiceImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, service_id, *args, **kwargs):
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(service=service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)