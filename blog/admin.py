"""
Configuration de l'interface admin pour le Blog
"""

from django.contrib import admin
from .models import Categorie, Tag, Article, Commentaire


# ============================================
# CATÉGORIE ADMIN
# ============================================

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """Configuration admin pour les catégories"""
    
    list_display = ['nom', 'slug', 'nombre_articles', 'ordre']
    list_editable = ['ordre']
    search_fields = ['nom', 'description']
    prepopulated_fields = {'slug': ('nom',)}  # Auto-génère le slug depuis le nom
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug', 'description')
        }),
        ('Paramètres', {
            'fields': ('ordre',)
        }),
    )


# ============================================
# TAG ADMIN
# ============================================

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Configuration admin pour les tags"""
    
    list_display = ['nom', 'slug', 'nombre_articles']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',)}


# ============================================
# COMMENTAIRE INLINE (pour l'afficher dans Article)
# ============================================

class CommentaireInline(admin.TabularInline):
    """Affiche les commentaires directement dans la page d'édition d'un article"""
    model = Commentaire
    extra = 0  # Ne pas afficher de formulaire vide
    fields = ['auteur_nom', 'contenu', 'approuve', 'date_creation']
    readonly_fields = ['date_creation']
    can_delete = True


# ============================================
# ARTICLE ADMIN
# ============================================

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Configuration admin pour les articles"""
    
    list_display = [
        'titre',
        'auteur',
        'categorie',
        'statut',
        'date_publication',
        'vues',
        'nombre_commentaires'
    ]
    
    list_filter = [
        'statut',
        'categorie',
        'date_publication',
        'auteur'
    ]
    
    search_fields = ['titre', 'contenu', 'extrait']
    
    prepopulated_fields = {'slug': ('titre',)}
    
    filter_horizontal = ['tags']  # Interface pratique pour les ManyToMany
    
    date_hierarchy = 'date_publication'
    
    readonly_fields = ['date_creation', 'date_modification', 'vues']
    
    list_per_page = 20
    
    # Affiche les commentaires dans la page de l'article
    inlines = [CommentaireInline]
    
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'slug', 'contenu', 'extrait', 'image')
        }),
        ('Classification', {
            'fields': ('categorie', 'tags')
        }),
        ('Publication', {
            'fields': ('auteur', 'statut', 'date_publication')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)  # Section repliée par défaut
        }),
        ('Statistiques', {
            'fields': ('vues', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Définit automatiquement l'auteur comme l'utilisateur connecté
        si c'est une création d'article
        """
        if not change:  # Si c'est une création (pas une modification)
            obj.auteur = request.user
        super().save_model(request, obj, form, change)


# ============================================
# COMMENTAIRE ADMIN
# ============================================

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    """Configuration admin pour les commentaires"""
    
    list_display = [
        'auteur_nom',
        'article',
        'contenu_court',
        'approuve',
        'date_creation'
    ]
    
    list_filter = ['approuve', 'date_creation']
    
    search_fields = ['auteur_nom', 'auteur_email', 'contenu']
    
    list_editable = ['approuve']  # Permet d'approuver depuis la liste
    
    readonly_fields = ['date_creation']
    
    date_hierarchy = 'date_creation'
    
    list_per_page = 50
    
    fieldsets = (
        ('Article', {
            'fields': ('article',)
        }),
        ('Auteur', {
            'fields': ('auteur_nom', 'auteur_email', 'auteur_user')
        }),
        ('Commentaire', {
            'fields': ('contenu', 'parent')
        }),
        ('Modération', {
            'fields': ('approuve', 'date_creation')
        }),
    )
    
    def contenu_court(self, obj):
        """Affiche un extrait du commentaire dans la liste"""
        if len(obj.contenu) > 50:
            return obj.contenu[:50] + "..."
        return obj.contenu
    contenu_court.short_description = "Contenu"
    
    actions = ['approuver_commentaires', 'refuser_commentaires']
    
    def approuver_commentaires(self, request, queryset):
        """Action pour approuver plusieurs commentaires d'un coup"""
        count = queryset.update(approuve=True)
        self.message_user(request, f"{count} commentaire(s) approuvé(s).")
    approuver_commentaires.short_description = "Approuver les commentaires sélectionnés"
    
    def refuser_commentaires(self, request, queryset):
        """Action pour refuser plusieurs commentaires d'un coup"""
        count = queryset.update(approuve=False)
        self.message_user(request, f"{count} commentaire(s) refusé(s).")
    refuser_commentaires.short_description = "Refuser les commentaires sélectionnés"