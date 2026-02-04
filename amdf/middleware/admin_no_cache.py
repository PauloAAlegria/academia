from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

# para não deixar nada em cache de memória da sessão de login do utilizador ao expirar o tempo de sessão
class AdminNoCacheMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path

        # Permitimos o acesso a login e logout
        if path.startswith('/admin/') and not request.user.is_authenticated:
            if not (path == reverse('admin:login') or path == reverse('admin:logout')):
                return HttpResponseRedirect(reverse('admin:login'))

    def process_response(self, request, response):
        if request.path.startswith('/admin/'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
