from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

# Serializador para registrar nuevos usuarios
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    # Agregar el campo business_type para que los usuarios seleccionen su tipo de negocio
    BUSINESS_CHOICES = (
        ('products', 'Productos'),
        ('services', 'Servicios'),
        ('both', 'Ambos'),
    )
    business_type = serializers.ChoiceField(choices=BUSINESS_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'user_type', 'business_name', 'business_type')  # Agregamos business_type

    def create(self, validated_data):
        # Usar create_user para que el manejo de contraseñas sea seguro
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # Deja que create_user maneje la contraseña
            user_type=validated_data['user_type'],
            business_name=validated_data.get('business_name', ''),
            business_type=validated_data['business_type']  # Guardamos el tipo de negocio
        )
        return user

# Serializador para ver y actualizar el perfil de usuario
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'business_name', 'whatsapp_number', 'facebook_page', 'business_type']
        read_only_fields = ['id', 'username', 'email']  # Campos que no se pueden editar