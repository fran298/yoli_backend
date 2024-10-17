from celery import shared_task
from time import sleep
from twilio.rest import Client

@shared_task
def delay_response(to_number, response_text, delay_time):
    sleep(delay_time)  # Retrasa la respuesta

    print(f"Respondiendo a {to_number} después de {delay_time} segundos.")
    return response_text    
    
    # Configura tu cliente de Twilio
    account_sid = 'AC01e981590b7ecd0b93f66001ebea9b0e'  # Reemplaza con tu SID de cuenta de Twilio
    auth_token = '53aee8fc4e794bc5b4edb6ab9c47a646'    # Reemplaza con tu token de autenticación de Twilio
    client = Client(account_sid, auth_token)

    # Envía el mensaje usando Twilio
    message = client.messages.create(
        body=response_text,
        from_='whatsapp:+14155238886',  # Tu número de WhatsApp de Twilio
        to=to_number
    )
    
    return f"Mensaje enviado a {to_number} con retraso de {delay_time} segundos"