from django.http import HttpResponseForbidden

def admin_only(get_response):
    def middleware(request):
        if request.user.is_authenticated and request.user.user_type == 'admin':
            return get_response(request)
        else:
            return HttpResponseForbidden("No tienes permisos para realizar esta acción.")
    return middleware