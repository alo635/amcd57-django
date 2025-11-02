from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .services import AnalyticsService, SystemHealthService, Fail2banService


@staff_member_required
def dashboard_view(request):
    """
    Vue principale du dashboard de monitoring (MVP).
    Affiche les statistiques de base du site sans graphiques.
    Réservé au staff uniquement.
    """

    # Statistiques visiteurs (7 et 30 jours)
    visitor_stats_7d = AnalyticsService.get_visitor_stats(days=7)
    visitor_stats_30d = AnalyticsService.get_visitor_stats(days=30)

    # Pages populaires
    popular_pages = AnalyticsService.get_popular_pages(limit=10)

    # Statistiques contenu
    content_stats = AnalyticsService.get_content_stats()

    # Santé système
    disk_usage = SystemHealthService.get_disk_usage()
    memory_usage = SystemHealthService.get_memory_usage()
    cpu_usage = SystemHealthService.get_cpu_usage()
    uptime = SystemHealthService.get_uptime()
    services_status = SystemHealthService.check_services()

    # Sécurité (basique pour MVP)
    banned_ips_count = Fail2banService.get_banned_ips_count()
    suspicious_ips = Fail2banService.get_recent_suspicious_ips(limit=10)

    context = {
        # Visiteurs
        'visitor_stats_7d': visitor_stats_7d,
        'visitor_stats_30d': visitor_stats_30d,
        'popular_pages': popular_pages,

        # Contenu
        'content_stats': content_stats,

        # Système
        'disk_usage': disk_usage,
        'memory_usage': memory_usage,
        'cpu_usage': cpu_usage,
        'uptime': uptime,
        'services_status': services_status,

        # Sécurité
        'banned_ips_count': banned_ips_count,
        'suspicious_ips': suspicious_ips,
    }

    return render(request, 'analytics/dashboard.html', context)
