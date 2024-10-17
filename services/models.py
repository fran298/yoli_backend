from django.db import models
from django.forms import ValidationError
from users.models import CustomUser


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()  # Duración del servicio (por ejemplo, 1 hora)
    category = models.CharField(max_length=255, blank=True, null=True)  # Mantener si es útil para la clasificación

    # Relacionar con el usuario que ofrece el servicio
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Relacionar con la empresa (opcional, si decides mantenerla)

    def __str__(self):
        return self.name

    # Validaciones adicionales
    def clean(self):
        if self.price <= 0:
            raise ValidationError('El precio debe ser mayor que cero.')

        if self.duration.total_seconds() <= 0:
            raise ValidationError('La duración debe ser mayor que cero.')

        # Validación opcional para 'category', si lo mantienes
        if self.category and len(self.category) > 255:
            raise ValidationError('La categoría no puede superar los 255 caracteres.')

# Modelo para manejar las imágenes de los servicios
class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services_images/')

    def __str__(self):
        return f"Imagen de {self.service.name}"