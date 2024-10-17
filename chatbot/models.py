from django.db import models
from users.models import CustomUser

class UserContext(models.Model):
    """
    Modelo para almacenar el contexto de la conversación con cada usuario.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    last_intent = models.CharField(max_length=100, blank=True, null=True)  # Última intención reconocida
    last_message = models.TextField(blank=True, null=True)  # Último mensaje enviado por el usuario
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contexto del usuario {self.user.username}"
    
class ChatMessage(models.Model):
    """
    Modelo para almacenar los mensajes enviados por el usuario y las respuestas del chatbot.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    context = models.ForeignKey(UserContext, on_delete=models.SET_NULL, null=True, blank=True)  # Contexto asociado
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.user.username} el {self.created_at}"