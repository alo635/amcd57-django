import time
from django.utils.deprecation import MiddlewareMixin
from .models import PageView


class AnalyticsMiddleware(MiddlewareMixin):
    """
    Middleware pour tracker automatiquement les visites de pages.
    Enregistre chaque requête GET dans la base de données pour analyse.
    """

    def process_request(self, request):
        """Enregistre l'heure de début de la requête"""
        request._start_time = time.time()

    def process_response(self, request, response):
        """Enregistre la page vue après traitement de la réponse"""

        # Ne pas tracker les requêtes admin, static, media
        if request.path.startswith(('/admin/', '/static/', '/media/', '/ckeditor/')):
            return response

        # Ne pas tracker les méthodes non-GET
        if request.method != 'GET':
            return response

        # Ne pas tracker les erreurs 404, 500, etc.
        if response.status_code >= 400:
            return response

        # Calculer le temps de réponse
        response_time = None
        if hasattr(request, '_start_time'):
            response_time = int((time.time() - request._start_time) * 1000)

        # Enregistrer la page vue (de manière asynchrone si possible)
        try:
            PageView.objects.create(
                url=request.path,
                user=request.user if request.user.is_authenticated else None,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referer=request.META.get('HTTP_REFERER', '')[:500],
                session_key=request.session.session_key or '',
                response_time=response_time,
            )
        except Exception as e:
            # Ne pas bloquer la requête si le tracking échoue
            # On pourrait logger l'erreur ici si nécessaire
            pass

        return response

    @staticmethod
    def get_client_ip(request):
        """
        Récupère l'IP réelle du client (même derrière proxy/load balancer).
        Regarde d'abord X-Forwarded-For, puis REMOTE_ADDR.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Prendre la première IP de la liste
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
