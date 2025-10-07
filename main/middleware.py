from django.shortcuts import redirect
from django.contrib import messages

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Login required sahifalarni tekshirish
        if request.path.startswith(('/super-admin/', '/administrator/', '/teacher/', '/student/')):
            if not request.session.get('user_id'):
                messages.error(request, 'Iltimos, avval tizimga kiring')
                return redirect('unified_login')
        
        response = self.get_response(request)
        return response