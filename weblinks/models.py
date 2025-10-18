"""
Modèles pour l'application Weblinks AMCD57
Gère l'annuaire de liens web organisés par catégories
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import URLValidator


# ============================================
# CATÉGORIE DE LIEN
# ============================================

class CategorieLien(models.Model):
    """
    Catégorie pour organiser les liens web
    (Officiels, Clubs, Techniques, Boutiques, etc.)
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la catégorie"
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    icone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icône",
        help_text="Nom de l'icône (ex: globe, link, star)"
    )
    
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les catégories avec un ordre plus petit apparaissent en premier"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Décocher pour masquer cette catégorie"
    )
    
    class Meta:
        verbose_name = "Catégorie de lien"
        verbose_name_plural = "Catégories de liens"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL de la catégorie"""
        return reverse('weblinks:categorie_detail', kwargs={'slug': self.slug})
    
    @property
    def nombre_liens(self):
        """Compte le nombre de liens actifs dans cette catégorie"""
        return self.liens.filter(actif=True).count()
    
    @property
    def liens_actifs(self):
        """Retourne les liens actifs de cette catégorie"""
        return self.liens.filter(actif=True).order_by('ordre', 'titre')


# ============================================
# LIEN
# ============================================

class Lien(models.Model):
    """
    Lien web vers un site externe
    """
    
    # Informations principales
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre du lien"
    )
    
    url = models.URLField(
        max_length=500,
        verbose_name="URL",
        validators=[URLValidator()],
        help_text="URL complète (ex: https://www.example.com)"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Description du site ou de la ressource"
    )
    
    # Catégorie
    categorie = models.ForeignKey(
        CategorieLien,
        on_delete=models.PROTECT,
        related_name='liens',
        verbose_name="Catégorie"
    )
    
    # Image/Logo
    logo = models.ImageField(
        upload_to='weblinks/logos/',
        null=True,
        blank=True,
        verbose_name="Logo du site",
        help_text="Logo ou capture d'écran du site"
    )
    
    # Métadonnées
    ajout_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='liens_ajoutes',
        verbose_name="Ajouté par"
    )
    
    date_ajout = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'ajout"
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    # Paramètres
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les liens avec un ordre plus petit apparaissent en premier"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Décocher pour masquer ce lien"
    )
    
    featured = models.BooleanField(
        default=False,
        verbose_name="Mis en avant",
        help_text="Cocher pour mettre ce lien en avant"
    )
    
    ouvrir_nouvel_onglet = models.BooleanField(
        default=True,
        verbose_name="Ouvrir dans un nouvel onglet",
        help_text="Ouvre le lien dans un nouvel onglet par défaut"
    )
    
    # Statistiques
    nombre_clics = models.IntegerField(
        default=0,
        verbose_name="Nombre de clics",
        editable=False
    )
    
    # Tags/Mots-clés
    tags = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Tags",
        help_text="Mots-clés séparés par des virgules (ex: planeur, thermique, moteur)"
    )
    
    # Notes administratives
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
        help_text="Notes internes (non visibles publiquement)"
    )
    
    class Meta:
        verbose_name = "Lien"
        verbose_name_plural = "Liens"
        ordering = ['categorie__ordre', 'ordre', 'titre']
        indexes = [
            models.Index(fields=['categorie', 'actif']),
            models.Index(fields=['featured']),
        ]
    
    def __str__(self):
        return f"{self.titre} ({self.categorie})"
    
    def get_absolute_url(self):
        """URL de redirection vers le lien"""
        return reverse('weblinks:lien_redirect', kwargs={'pk': self.pk})
    
    @property
    def domaine(self):
        """Extrait le nom de domaine de l'URL"""
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        return parsed.netloc.replace('www.', '')
    
    @property
    def liste_tags(self):
        """Retourne la liste des tags"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def incrementer_clics(self):
        """Incrémente le compteur de clics"""
        self.nombre_clics += 1
        self.save(update_fields=['nombre_clics'])
    
    def save(self, *args, **kwargs):
        # Nettoie l'URL (enlève les espaces)
        self.url = self.url.strip()
        super().save(*args, **kwargs)