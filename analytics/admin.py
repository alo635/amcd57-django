from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import PageView


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    """
    Administration pour les pages vues.
    Affiche les statistiques de visite en lecture seule.
    """
    list_display = [
        'get_short_url_display',
        'user',
        'ip_address',
        'timestamp',
        'response_time_display'
    ]
    list_filter = [
        'timestamp',
        ('user', admin.EmptyFieldListFilter),
    ]
    search_fields = [
        'url',
        'ip_address',
        'user__email'
    ]
    readonly_fields = [
        'url',
        'user',
        'ip_address',
        'user_agent',
        'referer',
        'session_key',
        'timestamp',
        'response_time'
    ]
    date_hierarchy = 'timestamp'
    list_per_page = 50
    ordering = ['-timestamp']

    def get_short_url_display(self, obj):
        """Affiche l'URL raccourcie"""
        return obj.get_short_url()
    get_short_url_display.short_description = "URL"

    def response_time_display(self, obj):
        """Affiche le temps de réponse avec code couleur"""
        if obj.response_time is None:
            return '-'

        # Code couleur selon le temps de réponse
        if obj.response_time < 100:
            color = 'green'
        elif obj.response_time < 500:
            color = 'orange'
        else:
            color = 'red'

        return format_html(
            '<span style="color: {};">{} ms</span>',
            color,
            obj.response_time
        )
    response_time_display.short_description = "Temps de réponse"

    def has_add_permission(self, request):
        """Empêche l'ajout manuel de pages vues (géré par middleware)"""
        return False

    def has_change_permission(self, request, obj=None):
        """Empêche la modification (données en lecture seule)"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Permet la suppression pour nettoyage des anciennes données"""
        return request.user.is_superuser


# Ajout d'un lien vers le dashboard dans l'index admin
def dashboard_link(request):
    """
    Retourne le lien HTML vers le dashboard de monitoring.
    À ajouter manuellement dans le template admin/index.html si souhaité.
    """
    url = reverse('analytics:dashboard')
    return format_html(
        '<a href="{}" class="btn btn-primary">Dashboard de Monitoring</a>',
        url
    )
