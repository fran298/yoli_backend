import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage
from products.models import Product
from services.models import Service
from users.models import CustomUser  # Asegúrate de importar el modelo de usuario
import spacy
import os  # Importamos la librería os para manejar la ruta
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse  # Para responder a Twilio

# Configuramos el logger para el monitoreo
logger = logging.getLogger('django')

# Ajustar la ruta para cargar el modelo correctamente
current_directory = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
model_path = os.path.join(current_directory, '..', 'chatbot', 'modelo_chatbot')
nlp = spacy.load(model_path)  # Cargar el modelo desde la ruta absoluta

class ChatbotView(APIView):
    """
    Vista principal del chatbot, maneja las interacciones con el cliente.
    El usuario debe estar autenticado para interactuar.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message', '').strip()

        if not user_message:
            return Response({"error": "No se recibió ningún mensaje."}, status=400)

        # Procesar el mensaje del usuario y generar la respuesta
        response_message = self.generate_response(user_message, request.user)

        try:
            # Guardar el mensaje y la respuesta
            chat_message = ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=response_message
            )
        except Exception as e:
            logger.error(f"Error al guardar el mensaje en la base de datos: {e}")
            return Response({"error": "No se pudo procesar el mensaje en este momento."}, status=500)

        return Response({"response": response_message})

    def generate_response(self, message, user):
        """
        Genera una respuesta usando NLP con spaCy para mejorar la detección de intención
        y filtrar los productos y servicios del usuario correspondiente.
        """
        # Procesar el mensaje con spaCy NLP
        try:
            doc = nlp(message.lower())
        except Exception as e:
            logger.error(f"Error al procesar el mensaje con spaCy: {e}")
            return "Lo siento, no pude entender tu mensaje."

        # Detectar la categoría principal según la intención
        if doc.cats:
            predicted_label = max(doc.cats, key=doc.cats.get)  # Obtener la categoría con mayor probabilidad

            if predicted_label == 'product_query':
                return self.handle_product_query(user)
            elif predicted_label == 'service_query':
                return self.handle_service_query(user)
            elif predicted_label == 'price_query':
                return "Para hacer una compra o consultar precios, por favor indica el nombre del producto o servicio."
            else:
                return "Lo siento, no entiendo esa consulta. ¿Podrías reformularla?"

        # Respuesta por defecto si no se detecta ninguna categoría
        return "Lo siento, no entiendo esa consulta. ¿Podrías reformularla?"

    def handle_product_query(self, user):
        """
        Maneja consultas sobre productos disponibles del usuario (emprendedor o pyme).
        """
        try:
            # Filtrar productos que pertenezcan al usuario actual
            products = Product.objects.filter(user=user, type='product')[:10]  # Limitar a los 10 primeros productos

            if products.exists():
                product_list = ', '.join([product.name for product in products])
                return f"Tenemos los siguientes productos disponibles: {product_list}"
            else:
                return "No tienes productos disponibles en este momento."
        except Exception as e:
            logger.error(f"Error al obtener productos: {e}")
            return "Hubo un error al buscar los productos. Intenta más tarde."

    def handle_service_query(self, user):
        """
        Maneja consultas sobre servicios disponibles del usuario (emprendedor o pyme).
        """
        try:
            # Filtrar servicios que pertenezcan al usuario actual
            services = Product.objects.filter(user=user, type='service')[:10]  # Limitar a los 10 primeros servicios

            if services.exists():
                service_list = ', '.join([f"{service.name} (ofrecido por {service.provider})" for service in services])
                return f"Ofrecemos los siguientes servicios: {service_list}"
            else:
                return "No tienes servicios disponibles en este momento."
        except Exception as e:
            logger.error(f"Error al obtener servicios: {e}")
            return "Hubo un error al buscar los servicios. Intenta más tarde."


# Aquí está la función `whatsapp_webhook` para manejar los mensajes entrantes de Twilio:
user_state = {}

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        message_body = request.POST.get('Body', '').lower()
        from_number = request.POST.get('From', '').replace('whatsapp:', '')  # Número de WhatsApp del cliente

        # Intentar encontrar al usuario por número de WhatsApp
        try:
            user = CustomUser.objects.get(whatsapp_number=from_number)
        except CustomUser.DoesNotExist:
            # Si no encontramos al usuario, no bloqueamos, solo continuamos sin un usuario asociado
            user = None

        # Si el usuario no tiene estado previo, inicializarlo
        if from_number not in user_state:
            user_state[from_number] = {
                'last_intent': None  # Para guardar la última intención detectada
            }

        # Procesar el mensaje con spaCy NLP
        doc = nlp(message_body)
        predicted_label = max(doc.cats, key=doc.cats.get)  # Categoría con mayor probabilidad

        response = MessagingResponse()

        # Manejamos la respuesta basada en el estado anterior del usuario
        last_intent = user_state[from_number]['last_intent']

        if predicted_label == 'product_query':
            if last_intent != 'product_query':
                response.message("Parece que estás interesado en nuestros productos. ¿Sobre cuál producto deseas más información?")
            else:
                # Si el usuario existe, mostramos sus productos; si no, mostramos productos generales
                if user:
                    products = Product.objects.filter(user=user, type='product')[:10]
                else:
                    products = Product.objects.filter(type='product')[:10]

                if products.exists():
                    product_list = ', '.join([product.name for product in products])
                    response.message(f"Los siguientes productos están disponibles: {product_list}")
                else:
                    response.message("No hay productos disponibles en este momento.")
            user_state[from_number]['last_intent'] = 'product_query'

        elif predicted_label == 'service_query':
            if last_intent != 'service_query':
                response.message("Parece que estás interesado en nuestros servicios. ¿Qué servicio te gustaría conocer más?")
            else:
                # Si el usuario existe, mostramos sus servicios; si no, mostramos servicios generales
                if user:
                    services = Product.objects.filter(user=user, type='service')[:10]
                else:
                    services = Product.objects.filter(type='service')[:10]

                if services.exists():
                    service_list = ', '.join([service.name for service in services])
                    response.message(f"Los siguientes servicios están disponibles: {service_list}")
                else:
                    response.message("No hay servicios disponibles en este momento.")
            user_state[from_number]['last_intent'] = 'service_query'

        elif predicted_label == 'price_query':
            response.message("Para hacer una compra o consultar precios, por favor indica el nombre del producto o servicio.")
            user_state[from_number]['last_intent'] = 'price_query'

        else:
            response.message("Lo siento, no entiendo esa consulta. ¿Podrías reformularla?")
            user_state[from_number]['last_intent'] = None

        return HttpResponse(str(response), content_type='text/xml')

    return HttpResponse(status=405)