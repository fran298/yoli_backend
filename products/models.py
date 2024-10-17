from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser

class Product(models.Model):
    SERVICE_TYPES = (
        ('product', 'Product'),
        ('service', 'Service'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=SERVICE_TYPES, default='product')
    stock = models.PositiveIntegerField(default=0)  # Para productos físicos, si aplica
    category = models.CharField(max_length=255, blank=True, null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Usuario relacionado

    def __str__(self):
        return self.name

    # Validaciones adicionales
    def clean(self):
        if self.price <= 0:
            raise ValidationError('El precio debe ser mayor que cero.')
        if self.stock < 0:
            raise ValidationError('El stock no puede ser negativo.')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  # Relación con Product
    image = models.ImageField(upload_to='products/')  # Subida de imágenes

    def __str__(self):
        return f"Imagen de {self.product.name}"