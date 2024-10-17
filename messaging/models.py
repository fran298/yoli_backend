from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, choices=[('servicios', 'Servicios'), ('productos', 'Productos')])
    numero_whatsapp = models.CharField(max_length=20, unique=True)  # Asegura que cada empresa tenga un número único

    def __str__(self):
        return self.nombre

class Message(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Enviado'),
        ('received', 'Recibido'),
        ('pending', 'Pendiente'),
    ]

    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')  # Estado por defecto

    def __str__(self):
        return f'Mensaje de {self.sender} a {self.recipient}'