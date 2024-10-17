from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('emprendedor', 'Emprendedor'),
        ('pyme', 'Pyme'),
        ('admin', 'Administrador'),
    )

    # Tipo de usuario (Emprendedor, Pyme o Administrador)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='emprendedor')

    # Nombre del negocio, solo para pymes o emprendedores
    business_name = models.CharField(max_length=255, blank=True, null=True)

    # Número de WhatsApp
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    # URL de la página de Facebook del negocio
    facebook_page = models.URLField(blank=True, null=True)

    # Seleccionar si vende productos, servicios o ambos
    BUSINESS_CHOICES = (
        ('products', 'Productos'),
        ('services', 'Servicios'),
        ('both', 'Ambos'),
    )
    business_type = models.CharField(max_length=10, choices=BUSINESS_CHOICES, default='both')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Evita conflicto con 'auth.User.groups'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Evita conflicto con 'auth.User.user_permissions'
        blank=True
    )

    def __str__(self):
        return self.username