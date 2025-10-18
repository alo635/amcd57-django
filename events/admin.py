"""
Configuration de l'interface admin pour Events
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import TypeEvenement, Lieu, Evenement, Inscription


# ============================================
# TYPE D'ÉVÉNEMENT ADMIN
# ============================================

@admin.register(TypeEvenement)
class TypeEvenementAdmin(admin.ModelAdmin):
    """Configuration admin pour les types d'événements"""
    
    list_display = ['nom', 'afficher_couleur', 'nombre_evenements', 'ordre', 'actif']
    list_editable = ['ordre', 'actif']
    list_filter = ['actif']
    search_fields = ['nom', 'description']
    prepopulated_fields = {'slug': ('nom',)}
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug', 'description')
        }),
        ('Apparence', {
            'fields': ('couleur', 'icone')
        }),
        ('Paramètres', {
            'fields': ('ordre', 'actif')
        }),
    )
    
    def afficher_couleur(self, obj):
        """Affiche un carré coloré avec la couleur du type"""
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border-radius: 4px;"></div>',
            obj.couleur
        )
    afficher_couleur.short_description = "Couleur"


# ============================================
# LIEU ADMIN
# ============================================

@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    """Configuration admin pour les lieux"""
    
    list_display = ['nom', 'ville', 'capacite', 'a_coordonnees_gps', 'actif']
    list_filter = ['actif', 'ville']
    search_fields = ['nom', 'adresse', 'ville']
    prepopulated_fields = {'slug': ('nom',)}
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug', 'description', 'image')
        }),
        ('Adresse', {
            'fields': ('adresse', 'code_postal', 'ville')
        }),
        ('Géolocalisation', {
            'fields': ('latitude', 'longitude'),
            'description': 'Coordonnées GPS pour affichage sur carte'
        }),
        ('Capacité', {
            'fields': ('capacite',)
        }),
        ('Paramètres', {
            'fields': ('actif',)
        }),
    )
    
    def a_coordonnees_gps(self, obj):
        """Icône indiquant si le lieu a des coordonnées GPS"""
        if obj.a_coordonnees_gps:
            return format_html('<span style="color: green;">✓ GPS</span>')
        return format_html('<span style="color: red;">✗ Pas de GPS</span>')
    a_coordonnees_gps.short_description = "Géolocalisation"


# ============================================
# INSCRIPTION INLINE (pour Événement)
# ============================================

class InscriptionInline(admin.TabularInline):
    """Affiche les inscriptions dans la page d'édition d'un événement"""
    model = Inscription
    extra = 0
    fields = ['participant', 'statut', 'nombre_accompagnants', 'present', 'date_inscription']
    readonly_fields = ['date_inscription']
    can_delete = True


# ============================================
# ÉVÉNEMENT ADMIN
# ============================================

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    """Configuration admin pour les événements"""
    
    list_display = [
        'titre',
        'type_evenement',
        'date_debut',
        'lieu',
        'statut_badge',
        'nombre_inscrits_display',
        'organisateur'
    ]
    
    list_filter = [
        'statut',
        'type_evenement',
        'date_debut',
        'inscription_requise',
        'public'
    ]
    
    search_fields = ['titre', 'description']
    
    prepopulated_fields = {'slug': ('titre',)}
    
    date_hierarchy = 'date_debut'
    
    readonly_fields = ['date_creation', 'date_modification', 'vues']
    
    list_per_page = 20
    
    inlines = [InscriptionInline]
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'slug', 'description', 'description_courte', 'image')
        }),
        ('Classification', {
            'fields': ('type_evenement',)
        }),
        ('Lieu', {
            'fields': ('lieu', 'lieu_details')
        }),
        ('Dates et horaires', {
            'fields': (
                'date_debut',
                'date_fin',
                'journee_complete'
            )
        }),
        ('Inscriptions', {
            'fields': (
                'inscription_requise',
                'places_limitees',
                'nombre_places',
                'date_limite_inscription'
            )
        }),
        ('Organisateur et statut', {
            'fields': ('organisateur', 'statut')
        }),
        ('Visibilité', {
            'fields': ('public', 'membres_seulement')
        }),
        ('Statistiques', {
            'fields': ('vues', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Définit automatiquement l'organisateur"""
        if not change:
            obj.organisateur = request.user
        super().save_model(request, obj, form, change)
    
    def statut_badge(self, obj):
        """Affiche le statut avec des couleurs"""
        colors = {
            'planifie': '#FFA500',
            'confirme': '#22C55E',
            'annule': '#EF4444',
            'termine': '#6B7280',
        }
        color = colors.get(obj.statut, '#6B7280')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_statut_display()
        )
    statut_badge.short_description = "Statut"
    
    def nombre_inscrits_display(self, obj):
        """Affiche le nombre d'inscrits"""
        if not obj.inscription_requise:
            return '-'
        
        nb = obj.nombre_inscrits
        
        if obj.places_limitees and obj.nombre_places:
            restantes = obj.places_restantes
            if restantes == 0:
                return format_html(
                    '<span style="color: red; font-weight: bold;">{}/{} (COMPLET)</span>',
                    nb, obj.nombre_places
                )
            return format_html('{}/{}', nb, obj.nombre_places)
        
        return str(nb)
    nombre_inscrits_display.short_description = "Inscrits"
    
    actions = ['marquer_termine', 'marquer_annule', 'marquer_confirme']
    
    def marquer_termine(self, request, queryset):
        """Action pour marquer des événements comme terminés"""
        count = queryset.update(statut='termine')
        self.message_user(request, f"{count} événement(s) marqué(s) comme terminé(s).")
    marquer_termine.short_description = "Marquer comme terminé"
    
    def marquer_annule(self, request, queryset):
        """Action pour annuler des événements"""
        count = queryset.update(statut='annule')
        self.message_user(request, f"{count} événement(s) annulé(s).")
    marquer_annule.short_description = "Marquer comme annulé"
    
    def marquer_confirme(self, request, queryset):
        """Action pour confirmer des événements"""
        count = queryset.update(statut='confirme')
        self.message_user(request, f"{count} événement(s) confirmé(s).")
    marquer_confirme.short_description = "Marquer comme confirmé"


# ============================================
# INSCRIPTION ADMIN
# ============================================

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    """Configuration admin pour les inscriptions"""
    
    list_display = [
        'participant',
        'evenement',
        'statut_badge',
        'nombre_accompagnants',
        'present',
        'date_inscription'
    ]
    
    list_filter = ['statut', 'present', 'evenement__type_evenement', 'date_inscription']
    
    search_fields = ['participant__username', 'participant__email', 'evenement__titre']
    
    list_editable = ['present']
    
    readonly_fields = ['date_inscription']
    
    date_hierarchy = 'date_inscription'
    
    list_per_page = 50
    
    fieldsets = (
        ('Événement', {
            'fields': ('evenement',)
        }),
        ('Participant', {
            'fields': ('participant', 'nombre_accompagnants', 'commentaire')
        }),
        ('Statut', {
            'fields': ('statut', 'present', 'date_inscription')
        }),
    )
    
    def statut_badge(self, obj):
        """Affiche le statut avec des couleurs"""
        colors = {
            'en_attente': '#FFA500',
            'confirme': '#22C55E',
            'annule': '#EF4444',
            'liste_attente': '#6B7280',
        }
        color = colors.get(obj.statut, '#6B7280')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_statut_display()
        )
    statut_badge.short_description = "Statut"
    
    actions = ['confirmer_inscriptions', 'annuler_inscriptions']
    
    def confirmer_inscriptions(self, request, queryset):
        """Action pour confirmer des inscriptions"""
        count = queryset.update(statut='confirme')
        self.message_user(request, f"{count} inscription(s) confirmée(s).")
    confirmer_inscriptions.short_description = "Confirmer les inscriptions"
    
    def annuler_inscriptions(self, request, queryset):
        """Action pour annuler des inscriptions"""
        count = queryset.update(statut='annule')
        self.message_user(request, f"{count} inscription(s) annulée(s).")
    annuler_inscriptions.short_description = "Annuler les inscriptions"