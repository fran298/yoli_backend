from rest_framework import serializers
from .models import Service, ServiceImage

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'category', 'provider']

    def create(self, validated_data):
        # Asignar automáticamente el usuario autenticado
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class ServiceImageSerializer(serializers.ModelSerializer):
    # Asegúrate de que el campo `service` esté relacionado correctamente
    class Meta:
        model = ServiceImage
        fields = ['id', 'image']

    def create(self, validated_data):
        # No es necesario agregar lógica extra aquí a menos que tengas validaciones especiales
        return super().create(validated_data)