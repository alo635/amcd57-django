"""
Configuration de l'interface admin pour Members
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils import timezone
from .models import TypeMembre, FonctionBureau, ProfilMembre


# ============================================
# TYPE DE MEMBRE ADMIN
# ============================================

@admin.register(TypeMembre)
class TypeMembreAdmin(admin.ModelAdmin):
    """Configuration admin pour les types de membres"""
    
    list_display = [
        'nom',
        'nombre_membres',
        'peut_voter',
        'acces_terrain',
        'acces_espace_membre',
        'ordre',
        'actif'
    ]
    
    list_editable = ['ordre', 'actif']
    list_filter = ['actif', 'peut_voter', 'acces_terrain']
    search_fields = ['nom', 'description']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'description', 'ordre')
        }),
        ('Droits et privilèges', {
            'fields': ('peut_voter', 'acces_terrain', 'acces_espace_membre')
        }),
        ('Paramètres', {
            'fields': ('actif',)
        }),
    )


# ============================================
# FONCTION BUREAU ADMIN
# ============================================

@admin.register(FonctionBureau)
class FonctionBureauAdmin(admin.ModelAdmin):
    """Configuration admin pour les fonctions bureau"""
    
    list_display = [
        'nom',
        'membre_actuel_display',
        'email_contact',
        'ordre',
        'actif'
    ]
    
    list_editable = ['ordre', 'actif']
    list_filter = ['actif']
    search_fields = ['nom', 'description']
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'description', 'ordre')
        }),
        ('Contact', {
            'fields': ('email_contact',)
        }),
        ('Paramètres', {
            'fields': ('actif',)
        }),
    )
    
    def membre_actuel_display(self, obj):
        """Affiche le membre qui occupe actuellement cette fonction"""
        membre = obj.membre_actuel
        if membre:
            return format_html(
                '<a href="/admin/members/profilmembre/{}/change/">{}</a>',
                membre.pk,
                membre.nom_complet
            )
        return format_html('<span style="color: #999;">Vacant</span>')
    membre_actuel_display.short_description = "Membre actuel"


# ============================================
# PROFIL MEMBRE INLINE (pour User)
# ============================================

class ProfilMembreInline(admin.StackedInline):
    """Affiche le profil membre dans la page d'édition d'un User"""
    model = ProfilMembre
    can_delete = False
    verbose_name_plural = 'Profil Membre'
    
    fieldsets = (
        ('Type et fonction', {
            'fields': ('type_membre', 'fonction_bureau', 'fonction_active')
        }),
        ('Informations personnelles', {
            'fields': ('photo', 'date_naissance', 'telephone', 'telephone_portable')
        }),
        ('Adresse', {
            'fields': ('adresse', 'code_postal', 'ville', 'pays'),
            'classes': ('collapse',)
        }),
        ('Aéromodélisme', {
            'fields': ('niveau', 'specialites', 'avions_possedes', 'experience_aeromodelisme')
        }),
        ('Licences et assurances', {
            'fields': (
                'numero_licence_ufolep',
                'date_validite_licence',
                'assurance_valide'
            )
        }),
        ('Adhésion', {
            'fields': ('date_adhesion', 'cotisation_a_jour', 'date_fin_cotisation')
        }),
        ('Préférences', {
            'fields': ('newsletter', 'notifications_evenements', 'profil_public'),
            'classes': ('collapse',)
        }),
        ('Réseaux sociaux', {
            'fields': ('site_web', 'youtube', 'facebook', 'instagram'),
            'classes': ('collapse',)
        }),
        ('Notes administratives', {
            'fields': ('notes_admin',),
            'classes': ('collapse',)
        }),
    )


# ============================================
# USER ADMIN ÉTENDU
# ============================================

class UserAdmin(BaseUserAdmin):
    """Extension de l'admin User pour inclure le ProfilMembre"""
    inlines = (ProfilMembreInline,)
    
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'type_membre_display',
        'cotisation_display',
        'is_staff'
    ]
    
    list_filter = BaseUserAdmin.list_filter + ('profil__type_membre', 'profil__cotisation_a_jour')
    
    def type_membre_display(self, obj):
        """Affiche le type de membre"""
        if hasattr(obj, 'profil'):
            return obj.profil.type_membre
        return '-'
    type_membre_display.short_description = "Type"
    
    def cotisation_display(self, obj):
        """Affiche le statut de cotisation"""
        if hasattr(obj, 'profil'):
            if obj.profil.cotisation_a_jour:
                return format_html(
                    '<span style="color: green; font-weight: bold;">✓ À jour</span>'
                )
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Expirée</span>'
            )
        return '-'
    cotisation_display.short_description = "Cotisation"


# Désinscrire l'admin User par défaut et inscrire le nôtre
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ============================================
# PROFIL MEMBRE ADMIN (vue dédiée)
# ============================================

@admin.register(ProfilMembre)
class ProfilMembreAdmin(admin.ModelAdmin):
    """Configuration admin pour les profils membres (vue séparée)"""
    
    list_display = [
        'nom_complet',
        'type_membre',
        'fonction_bureau_badge',
        'niveau',
        'cotisation_badge',
        'assurance_badge',
        'date_adhesion'
    ]
    
    list_filter = [
        'type_membre',
        'fonction_bureau',
        'niveau',
        'cotisation_a_jour',
        'assurance_valide',
        'date_adhesion'
    ]
    
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'telephone',
        'ville'
    ]
    
    readonly_fields = ['date_creation', 'date_modification', 'age', 'anciennete_annees']
    
    date_hierarchy = 'date_adhesion'
    
    list_per_page = 50
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Type et fonction', {
            'fields': ('type_membre', 'fonction_bureau', 'fonction_active')
        }),
        ('Informations personnelles', {
            'fields': (
                'photo',
                'date_naissance',
                'age',
                'telephone',
                'telephone_portable'
            )
        }),
        ('Adresse', {
            'fields': ('adresse', 'code_postal', 'ville', 'pays')
        }),
        ('Biographie', {
            'fields': ('bio', 'experience_aeromodelisme'),
            'classes': ('collapse',)
        }),
        ('Aéromodélisme', {
            'fields': ('niveau', 'specialites', 'avions_possedes')
        }),
        ('Licences et assurances', {
            'fields': (
                'numero_licence_ufolep',
                'date_validite_licence',
                'assurance_valide'
            )
        }),
        ('Adhésion', {
            'fields': (
                'date_adhesion',
                'anciennete_annees',
                'cotisation_a_jour',
                'date_fin_cotisation'
            )
        }),
        ('Préférences', {
            'fields': (
                'newsletter',
                'notifications_evenements',
                'profil_public'
            ),
            'classes': ('collapse',)
        }),
        ('Réseaux sociaux', {
            'fields': ('site_web', 'youtube', 'facebook', 'instagram'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
        ('Notes administratives', {
            'fields': ('notes_admin',),
            'classes': ('collapse',)
        }),
    )
    
    def fonction_bureau_badge(self, obj):
        """Affiche un badge pour la fonction bureau"""
        if obj.est_membre_bureau:
            return format_html(
                '<span style="background-color: #3B82F6; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">👔 {}</span>',
                obj.fonction_bureau
            )
        return '-'
    fonction_bureau_badge.short_description = "Fonction"
    
    def cotisation_badge(self, obj):
        """Affiche un badge pour le statut de cotisation"""
        if obj.cotisation_a_jour:
            couleur = '#22C55E'
            texte = '✓ À jour'
        else:
            couleur = '#EF4444'
            texte = '✗ Expirée'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            couleur, texte
        )
    cotisation_badge.short_description = "Cotisation"
    
    def assurance_badge(self, obj):
        """Affiche un badge pour le statut d'assurance"""
        if obj.assurance_valide:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗</span>'
        )
    assurance_badge.short_description = "Assurance"
    
    actions = [
        'mettre_cotisation_a_jour',
        'marquer_cotisation_expiree',
        'activer_assurance',
        'desactiver_assurance'
    ]
    
    def mettre_cotisation_a_jour(self, request, queryset):
        """Action pour mettre les cotisations à jour"""
        from datetime import timedelta
        today = timezone.now().date()
        
        count = 0
        for profil in queryset:
            profil.date_fin_cotisation = today + timedelta(days=365)
            profil.cotisation_a_jour = True
            profil.save()
            count += 1
        
        self.message_user(
            request,
            f"{count} cotisation(s) mise(s) à jour jusqu'au {(today + timedelta(days=365)).strftime('%d/%m/%Y')}."
        )
    mettre_cotisation_a_jour.short_description = "Mettre les cotisations à jour (1 an)"
    
    def marquer_cotisation_expiree(self, request, queryset):
        """Action pour marquer les cotisations comme expirées"""
        count = queryset.update(cotisation_a_jour=False)
        self.message_user(request, f"{count} cotisation(s) marquée(s) comme expirée(s).")
    marquer_cotisation_expiree.short_description = "Marquer cotisations expirées"
    
    def activer_assurance(self, request, queryset):
        """Action pour activer l'assurance"""
        count = queryset.update(assurance_valide=True)
        self.message_user(request, f"{count} assurance(s) activée(s).")
    activer_assurance.short_description = "Activer l'assurance"
    
    def desactiver_assurance(self, request, queryset):
        """Action pour désactiver l'assurance"""
        count = queryset.update(assurance_valide=False)
        self.message_user(request, f"{count} assurance(s) désactivée(s).")
    desactiver_assurance.short_description = "Désactiver l'assurance"