import random
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from .tasks import delay_response  # Importamos la tarea de Celery
import spacy

# Cargar el modelo de NLP entrenado
nlp = spacy.load('modelo_chatbot')

# Procesar el mensaje usando el modelo NLP
def process_message_with_nlp(message):
    doc = nlp(message)
    predicted_label = max(doc.cats, key=doc.cats.get)

    if predicted_label == 'product_query':
        return "Aquí tienes información sobre nuestros productos. ¿Cuál te interesa?"
    elif predicted_label == 'service_query':
        return "Ofrecemos servicios como instalación y mantenimiento. ¿En qué te puedo ayudar?"
    elif predicted_label == 'price_query':
        return "Los precios varían según el producto. ¿Sobre cuál te gustaría saber más?"
    else:
        return "Lo siento, no entendí tu consulta. ¿Puedes reformularla?"

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        message_body = request.POST.get('Body', '').lower()
        from_number = request.POST.get('From', '')  # Número de WhatsApp del cliente
        print(f"Número recibido: {from_number}")

        # Procesar el mensaje de manera simple y devolver una respuesta
        response = MessagingResponse()
        response.message("Gracias por tu mensaje. Te responderemos pronto.")
        return HttpResponse(str(response), content_type='text/xml')

    return HttpResponse("Método no permitido", status=405)