from django.urls import path
from . import views

urlpatterns = [
    path('whatsapp/messaging-webhook/', views.whatsapp_webhook, name='whatsapp_webhook_messaging'),
]