from datetime import timedelta
from messaging.models import Empresa
from services.models import Service
from users.models import CustomUser

# En el método setUp del archivo chatbot/tests.py
def setUp(self):
    self.user = CustomUser.objects.create_user(username="testuser", password="testpass")
    self.empresa = Empresa.objects.create(nombre="Test Empresa")
    
    # Agregar el valor de duration
    self.service = Service.objects.create(
        name="Test Servicio",
        price=200,
        duration=timedelta(hours=1),  # Asegúrate de incluir una duración
        user=self.user,
        company=self.empresa
    )