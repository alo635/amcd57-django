"""
Configuration de l'interface admin pour Weblinks
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import CategorieLien, Lien


# ============================================
# CATÉGORIE DE LIEN ADMIN
# ============================================

@admin.register(CategorieLien)
class CategorieLienAdmin(admin.ModelAdmin):
    """Configuration admin pour les catégories de liens"""
    
    list_display = ['nom', 'nombre_liens', 'icone', 'ordre', 'actif']
    list_editable = ['ordre', 'actif']
    list_filter = ['actif']
    search_fields = ['nom', 'description']
    prepopulated_fields = {'slug': ('nom',)}
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug', 'description')
        }),
        ('Apparence', {
            'fields': ('icone',)
        }),
        ('Paramètres', {
            'fields': ('ordre', 'actif')
        }),
    )


# ============================================
# LIEN ADMIN
# ============================================

@admin.register(Lien)
class LienAdmin(admin.ModelAdmin):
    """Configuration admin pour les liens"""
    
    list_display = [
        'titre',
        'domaine_display',
        'categorie',
        'featured_badge',
        'nombre_clics',
        'ordre',
        'actif'
    ]
    
    list_filter = [
        'categorie',
        'featured',
        'actif',
        'date_ajout'
    ]
    
    search_fields = ['titre', 'description', 'url', 'tags']
    
    list_editable = ['ordre', 'actif']
    
    readonly_fields = ['date_ajout', 'date_modification', 'nombre_clics', 'ajout_par']
    
    date_hierarchy = 'date_ajout'
    
    list_per_page = 50
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'url', 'description', 'logo')
        }),
        ('Classification', {
            'fields': ('categorie', 'tags')
        }),
        ('Paramètres', {
            'fields': (
                'ordre',
                'actif',
                'featured',
                'ouvrir_nouvel_onglet'
            )
        }),
        ('Métadonnées', {
            'fields': ('ajout_par', 'date_ajout', 'date_modification'),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('nombre_clics',),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Définit automatiquement l'utilisateur qui ajoute le lien"""
        if not change:  # Nouvelle création
            obj.ajout_par = request.user
        super().save_model(request, obj, form, change)
    
    def domaine_display(self, obj):
        """Affiche le domaine du lien"""
        return format_html(
            '<a href="{}" target="_blank" style="color: #3B82F6;">{}</a>',
            obj.url,
            obj.domaine
        )
    domaine_display.short_description = "Domaine"
    
    def featured_badge(self, obj):
        """Affiche un badge pour les liens mis en avant"""
        if obj.featured:
            return format_html(
                '<span style="background-color: #F59E0B; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">⭐ Mis en avant</span>'
            )
        return '-'
    featured_badge.short_description = "Statut"
    
    actions = ['marquer_featured', 'retirer_featured', 'activer_liens', 'desactiver_liens']
    
    def marquer_featured(self, request, queryset):
        """Action pour mettre des liens en avant"""
        count = queryset.update(featured=True)
        self.message_user(request, f"{count} lien(s) marqué(s) comme mis en avant.")
    marquer_featured.short_description = "Mettre en avant"
    
    def retirer_featured(self, request, queryset):
        """Action pour retirer la mise en avant"""
        count = queryset.update(featured=False)
        self.message_user(request, f"{count} lien(s) retiré(s) de la mise en avant.")
    retirer_featured.short_description = "Retirer la mise en avant"
    
    def activer_liens(self, request, queryset):
        """Action pour activer des liens"""
        count = queryset.update(actif=True)
        self.message_user(request, f"{count} lien(s) activé(s).")
    activer_liens.short_description = "Activer les liens"
    
    def desactiver_liens(self, request, queryset):
        """Action pour désactiver des liens"""
        count = queryset.update(actif=False)
        self.message_user(request, f"{count} lien(s) désactivé(s).")
    desactiver_liens.short_description = "Désactiver les liens"