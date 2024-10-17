# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Importa tu modelo CustomUser

# Registra el modelo CustomUser en el panel de administración
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Definimos los campos que queremos mostrar en la lista de usuarios en el admin
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Campos que queremos ver en el formulario de detalle de un usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('email', 'user_type', 'business_name', 'whatsapp_number', 'facebook_page')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos que se muestran cuando creamos un nuevo usuario en el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active')}
        ),
    )