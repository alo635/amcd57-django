"""
Configuration de l'interface admin pour Core
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ContactMessage


# ============================================
# MESSAGE DE CONTACT ADMIN
# ============================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Configuration admin pour les messages de contact"""
    
    list_display = [
        'nom_complet',
        'email',
        'sujet_badge',
        'statut_badge',
        'lu_badge',
        'repondu_badge',
        'age_message_display',
        'date_envoi'
    ]
    
    list_filter = [
        'statut',
        'sujet',
        'lu',
        'repondu',
        'date_envoi'
    ]
    
    search_fields = ['nom', 'prenom', 'email', 'message']
    
    readonly_fields = [
        'date_envoi',
        'ip_address',
        'age_message',
        'date_traitement',
        'date_reponse'
    ]
    
    date_hierarchy = 'date_envoi'
    
    list_per_page = 50
    
    fieldsets = (
        ('Informations du contact', {
            'fields': ('nom', 'prenom', 'email', 'telephone')
        }),
        ('Message', {
            'fields': ('sujet', 'message')
        }),
        ('Métadonnées', {
            'fields': ('date_envoi', 'ip_address', 'age_message')
        }),
        ('Gestion', {
            'fields': ('statut', 'lu', 'date_traitement')
        }),
        ('Réponse', {
            'fields': ('reponse', 'repondu', 'date_reponse')
        }),
        ('Notes internes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def sujet_badge(self, obj):
        """Affiche le sujet avec un badge coloré"""
        colors = {
            'info': '#3B82F6',
            'adhesion': '#10B981',
            'evenement': '#F59E0B',
            'technique': '#8B5CF6',
            'partenariat': '#EC4899',
            'autre': '#6B7280',
        }
        color = colors.get(obj.sujet, '#6B7280')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_sujet_display()
        )
    sujet_badge.short_description = "Sujet"
    
    def statut_badge(self, obj):
        """Affiche le statut avec un badge coloré"""
        colors = {
            'nouveau': '#EF4444',
            'en_cours': '#F59E0B',
            'traite': '#22C55E',
            'archive': '#6B7280',
        }
        color = colors.get(obj.statut, '#6B7280')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_statut_display()
        )
    statut_badge.short_description = "Statut"
    
    def lu_badge(self, obj):
        """Affiche si le message est lu"""
        if obj.lu:
            return format_html('<span style="color: green; font-weight: bold;">✓</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗</span>')
    lu_badge.short_description = "Lu"
    
    def repondu_badge(self, obj):
        """Affiche si le message a été répondu"""
        if obj.repondu:
            return format_html('<span style="color: green; font-weight: bold;">✓</span>')
        return format_html('<span style="color: #999;">-</span>')
    repondu_badge.short_description = "Répondu"
    
    def age_message_display(self, obj):
        """Affiche l'âge du message"""
        age = obj.age_message
        if age == 0:
            return "Aujourd'hui"
        elif age == 1:
            return "Hier"
        elif age < 7:
            return f"Il y a {age} jours"
        elif age < 30:
            semaines = age // 7
            return f"Il y a {semaines} semaine{'s' if semaines > 1 else ''}"
        else:
            mois = age // 30
            return f"Il y a {mois} mois"
    age_message_display.short_description = "Âge"
    
    actions = [
        'marquer_lu',
        'marquer_non_lu',
        'marquer_traite',
        'marquer_en_cours',
        'archiver'
    ]
    
    def marquer_lu(self, request, queryset):
        """Action pour marquer des messages comme lus"""
        count = queryset.update(lu=True)
        self.message_user(request, f"{count} message(s) marqué(s) comme lu(s).")
    marquer_lu.short_description = "Marquer comme lu"
    
    def marquer_non_lu(self, request, queryset):
        """Action pour marquer des messages comme non lus"""
        count = queryset.update(lu=False)
        self.message_user(request, f"{count} message(s) marqué(s) comme non lu(s).")
    marquer_non_lu.short_description = "Marquer comme non lu"
    
    def marquer_traite(self, request, queryset):
        """Action pour marquer des messages comme traités"""
        now = timezone.now()
        count = 0
        for message in queryset:
            message.statut = 'traite'
            message.date_traitement = now
            message.lu = True
            message.save()
            count += 1
        self.message_user(request, f"{count} message(s) marqué(s) comme traité(s).")
    marquer_traite.short_description = "Marquer comme traité"
    
    def marquer_en_cours(self, request, queryset):
        """Action pour marquer des messages en cours"""
        count = queryset.update(statut='en_cours', lu=True)
        self.message_user(request, f"{count} message(s) marqué(s) en cours.")
    marquer_en_cours.short_description = "Marquer en cours"
    
    def archiver(self, request, queryset):
        """Action pour archiver des messages"""
        count = queryset.update(statut='archive')
        self.message_user(request, f"{count} message(s) archivé(s).")
    archiver.short_description = "Archiver"
    
    def has_add_permission(self, request):
        """Désactive l'ajout manuel de messages via l'admin"""
        return False