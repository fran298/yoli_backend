from rest_framework import generics
from users.models import CustomUser
from .serializers import RegisterSerializer, CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

# Vista para registrar nuevos usuarios
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Vista para ver y actualizar el perfil de usuario autenticado
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vista para obtener y actualizar el perfil de usuario.
    Solo usuarios autenticados pueden acceder a su propio perfil.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retornamos el usuario autenticado
        return self.request.user