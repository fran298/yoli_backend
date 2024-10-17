from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    # Incluir el serializador de imágenes
    images = ProductImageSerializer(many=True, read_only=True)  # Lectura de las imágenes asociadas
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )  # Para manejar la subida de múltiples imágenes

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'type', 'stock', 'images', 'uploaded_images']

    def create(self, validated_data):
        # Eliminar las imágenes subidas del validated_data
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        # Asignar el usuario autenticado
        request = self.context.get('request')
        validated_data['user'] = request.user
        
        # Crear el producto
        product = super().create(validated_data)
        
        # Subir las imágenes
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        
        return product

    def update(self, instance, validated_data):
        # Eliminar las imágenes subidas del validated_data
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        # Actualizar los demás campos del producto
        product = super().update(instance, validated_data)
        
        # Subir las imágenes (si se han proporcionado nuevas)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        
        return product