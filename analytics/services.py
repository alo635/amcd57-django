import psutil
import time
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from .models import PageView

# Import des modèles des autres apps
try:
    from blog.models import Article
except ImportError:
    Article = None

try:
    from events.models import Evenement
except ImportError:
    Evenement = None

User = get_user_model()


class AnalyticsService:
    """Service pour récupérer les statistiques du site"""

    @staticmethod
    def get_visitor_stats(days=30):
        """
        Statistiques de visiteurs sur N jours.
        Retourne le nombre de pages vues, visiteurs uniques, et moyenne pages/visiteur.
        """
        since = timezone.now() - timedelta(days=days)

        total_views = PageView.objects.filter(timestamp__gte=since).count()
        unique_visitors = PageView.objects.filter(
            timestamp__gte=since
        ).values('ip_address').distinct().count()

        return {
            'total_views': total_views,
            'unique_visitors': unique_visitors,
            'avg_views_per_visitor': round(total_views / unique_visitors, 1) if unique_visitors > 0 else 0,
        }

    @staticmethod
    def get_popular_pages(limit=10):
        """
        Pages les plus consultées.
        Retourne les URLs avec leur nombre de vues.
        """
        return PageView.objects.values('url').annotate(
            views=Count('id')
        ).order_by('-views')[:limit]

    @staticmethod
    def get_content_stats():
        """
        Statistiques sur le contenu du site.
        Retourne le nombre d'articles, événements, membres, etc.
        """
        stats = {
            'total_members': User.objects.filter(is_active=True).count(),
        }

        # Articles (si l'app blog est installée)
        if Article:
            stats['total_articles'] = Article.objects.filter(statut='publie').count()
            stats['popular_articles'] = Article.objects.filter(
                statut='publie'
            ).order_by('-vues')[:5]
        else:
            stats['total_articles'] = 0
            stats['popular_articles'] = []

        # Événements (si l'app events est installée)
        if Evenement:
            stats['total_events'] = Evenement.objects.count()
        else:
            stats['total_events'] = 0

        return stats


class SystemHealthService:
    """Service pour la santé du système"""

    @staticmethod
    def get_disk_usage():
        """
        Utilisation du disque.
        Retourne l'espace total, utilisé, libre et le pourcentage.
        """
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
        }

    @staticmethod
    def get_memory_usage():
        """
        Utilisation de la RAM.
        Retourne la mémoire totale, disponible, utilisée et le pourcentage.
        """
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
        }

    @staticmethod
    def get_cpu_usage():
        """
        Utilisation du CPU.
        Retourne le pourcentage d'utilisation et le nombre de cœurs.
        """
        return {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
        }

    @staticmethod
    def get_uptime():
        """
        Uptime du serveur.
        Retourne le temps de fonctionnement en secondes et formaté.
        """
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        return {
            'seconds': int(uptime_seconds),
            'formatted': str(timedelta(seconds=int(uptime_seconds))),
        }

    @staticmethod
    def check_services():
        """
        Vérifier si les services sont actifs.
        Retourne un dict avec le statut de chaque service (True/False).
        """
        services = {
            'gunicorn': False,
            'nginx': False,
            'fail2ban': False,
        }

        # Parcourir tous les processus actifs
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()

                # Vérifier Gunicorn
                if 'gunicorn' in proc_name:
                    services['gunicorn'] = True

                # Vérifier Nginx
                if 'nginx' in proc_name:
                    services['nginx'] = True

                # Vérifier Fail2ban
                if 'fail2ban' in proc_name:
                    services['fail2ban'] = True

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Ignorer les processus qui n'existent plus ou inaccessibles
                pass

        return services


class Fail2banService:
    """Service pour les métriques Fail2ban (basique pour MVP)"""

    @staticmethod
    def get_banned_ips_count():
        """
        Nombre d'IPs uniques bannies dans l'historique.
        Pour le MVP, on simule avec les IPs qui ont généré beaucoup d'erreurs.
        """
        # Pour le MVP, on compte les IPs qui ont fait plus de 10 requêtes
        # Dans Phase 2, on parsera le vrai log Fail2ban
        suspicious_ips = PageView.objects.values('ip_address').annotate(
            count=Count('id')
        ).filter(count__gte=50).count()

        return suspicious_ips

    @staticmethod
    def get_recent_suspicious_ips(limit=10):
        """
        Liste des IPs les plus actives (potentiellement suspectes).
        Pour le MVP, on liste les IPs avec le plus de requêtes.
        """
        suspicious = PageView.objects.values('ip_address').annotate(
            request_count=Count('id')
        ).order_by('-request_count')[:limit]

        return list(suspicious)
