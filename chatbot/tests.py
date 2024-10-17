from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from products.models import Product
from services.models import Service
from messaging.models import Empresa
from chatbot.models import ChatMessage
from datetime import timedelta

class ChatbotTestCase(TestCase):

    def setUp(self):
        # Crear un usuario para autenticar las solicitudes
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

        # Crear una empresa de prueba
        self.empresa = Empresa.objects.create(nombre="Test Empresa")

        # Crear un producto y servicio de prueba
        self.product = Product.objects.create(
            name="Test Producto", 
            price=100, 
            user=self.user, 
            company=self.empresa
        )
        self.service = Service.objects.create(
            name="Test Servicio", 
            price=200, 
            duration=timedelta(hours=1),  # Asegúrate de incluir la duración
            user=self.user, 
            company=self.empresa
        )

    def test_chatbot_greeting(self):
        """Prueba de saludo básico del chatbot"""
        response = self.client.post(reverse('chatbot'), {'message': 'hola'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Hola', response.data['response'])

    def test_chatbot_product_query(self):
        """Prueba de consulta de productos"""
        response = self.client.post(reverse('chatbot'), {'message': 'quiero un producto'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Producto', response.data['response'])

    def test_chatbot_service_query(self):
        """Prueba de consulta de servicios"""
        response = self.client.post(reverse('chatbot'), {'message': 'quiero un servicio'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Servicio', response.data['response'])

    def test_chatbot_unknown_message(self):
        """Prueba para mensajes desconocidos o no reconocidos"""
        response = self.client.post(reverse('chatbot'), {'message': 'random message'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('no entiendo', response.data['response'])

    def test_chat_message_saved(self):
        """Prueba para verificar que los mensajes se guardan en la base de datos"""
        self.client.post(reverse('chatbot'), {'message': 'hola'})
        self.assertTrue(ChatMessage.objects.filter(user=self.user).exists())