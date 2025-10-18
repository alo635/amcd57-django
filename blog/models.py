"""
Modèles pour l'application Blog AMCD57
Gère les catégories, tags, articles et commentaires
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


# ============================================
# CATÉGORIE
# ============================================

class Categorie(models.Model):
    """
    Catégorie d'article (Club, Technique, Convention, Divers)
    Relation: Une catégorie → Plusieurs articles
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
    
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les catégories avec un ordre plus petit apparaissent en premier"
    )
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        """Auto-génération du slug si vide"""
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL de la catégorie"""
        return reverse('blog:categorie_detail', kwargs={'slug': self.slug})
    
    @property
    def nombre_articles(self):
        """Compte le nombre d'articles publiés dans cette catégorie"""
        return self.articles.filter(statut='publie').count()


# ============================================
# TAG
# ============================================

class Tag(models.Model):
    """
    Étiquette d'article (mots-clés)
    Relation: Plusieurs tags ↔ Plusieurs articles (ManyToMany)
    """
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom du tag"
    )
    
    slug = models.SlugField(
        max_length=50,
        unique=True
    )
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL du tag"""
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})
    
    @property
    def nombre_articles(self):
        """Compte le nombre d'articles publiés avec ce tag"""
        return self.articles.filter(statut='publie').count()


# ============================================
# ARTICLE
# ============================================

class Article(models.Model):
    """
    Article de blog
    Relations:
    - Un article → Une catégorie (ForeignKey)
    - Un article → Un auteur (ForeignKey vers User)
    - Un article ↔ Plusieurs tags (ManyToMany)
    """
    
    # Statuts possibles (brouillon/publié)
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]
    
    # Champs principaux
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug (URL)"
    )
    
    contenu = models.TextField(
        verbose_name="Contenu",
        help_text="Contenu de l'article (supporte le HTML)"
    )
    
    extrait = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Extrait",
        help_text="Résumé court pour la liste des articles (généré auto si vide)"
    )
    
    # Relations
    auteur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name="Auteur"
    )
    
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,  # Empêche suppression si articles existent
        related_name='articles',
        verbose_name="Catégorie"
    )
    
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles',
        verbose_name="Tags"
    )
    
    # Image à la une
    image = models.ImageField(
        upload_to='blog/articles/%Y/%m/',  # Organisé par année/mois
        null=True,
        blank=True,
        verbose_name="Image à la une",
        help_text="Image principale de l'article"
    )
    
    # Dates
    date_creation = models.DateTimeField(
        auto_now_add=True,  # Date de création automatique
        verbose_name="Date de création"
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,  # Mise à jour automatique
        verbose_name="Date de modification"
    )
    
    date_publication = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de publication"
    )
    
    # Statut
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='brouillon',
        verbose_name="Statut"
    )
    
    # Statistiques
    vues = models.IntegerField(
        default=0,
        verbose_name="Nombre de vues",
        editable=False  # Non modifiable dans l'admin
    )
    
    # SEO (pour plus tard)
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta description",
        help_text="Description pour les moteurs de recherche (max 160 car.)"
    )
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-date_publication', '-date_creation']
        indexes = [
            models.Index(fields=['-date_publication']),
            models.Index(fields=['statut']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        """Auto-génération du slug et gestion de la publication"""
        # Génère le slug si vide
        if not self.slug:
            self.slug = slugify(self.titre)
            # Vérifie l'unicité du slug
            original_slug = self.slug
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Si on publie l'article et qu'il n'a pas de date de publication
        if self.statut == 'publie' and not self.date_publication:
            self.date_publication = timezone.now()
        
        # Génère un extrait automatique si vide
        if not self.extrait and self.contenu:
            # Prend les 150 premiers caractères du contenu
            self.extrait = self.contenu[:150] + "..."
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL de l'article"""
        return reverse('blog:article_detail', kwargs={'slug': self.slug})
    
    @property
    def est_publie(self):
        """Vérifie si l'article est publié"""
        return self.statut == 'publie'
    
    @property
    def nombre_commentaires(self):
        """Compte le nombre de commentaires approuvés"""
        return self.commentaires.filter(approuve=True).count()
    
    def incrementer_vues(self):
        """Incrémente le compteur de vues"""
        self.vues += 1
        self.save(update_fields=['vues'])
    
    def est_recent(self, jours=7):
        """Vérifie si l'article a été publié récemment"""
        if self.date_publication:
            from datetime import timedelta
            return timezone.now() - self.date_publication < timedelta(days=jours)
        return False


# ============================================
# COMMENTAIRE
# ============================================

class Commentaire(models.Model):
    """
    Commentaire sur un article
    Relation: Un commentaire → Un article (ForeignKey)
    """
    
    # Relation avec l'article
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='commentaires',
        verbose_name="Article"
    )
    
    # Auteur (peut être un visiteur non inscrit)
    auteur_nom = models.CharField(
        max_length=100,
        verbose_name="Nom de l'auteur"
    )
    
    auteur_email = models.EmailField(
        verbose_name="Email de l'auteur"
    )
    
    # Si l'auteur est un membre connecté
    auteur_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commentaires',
        verbose_name="Membre"
    )
    
    # Contenu
    contenu = models.TextField(
        verbose_name="Commentaire"
    )
    
    # Dates
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    # Modération
    approuve = models.BooleanField(
        default=False,
        verbose_name="Approuvé ?",
        help_text="Les commentaires doivent être approuvés avant d'apparaître"
    )
    
    # Optionnel : système de réponses
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reponses',
        verbose_name="Réponse à"
    )
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['date_creation']
        indexes = [
            models.Index(fields=['article', 'approuve']),
        ]
    
    def __str__(self):
        return f"Commentaire de {self.auteur_nom} sur {self.article.titre}"
    
    def get_nom_auteur(self):
        """Retourne le nom de l'auteur (membre ou visiteur)"""
        if self.auteur_user:
            return f"{self.auteur_user.first_name} {self.auteur_user.last_name}" or self.auteur_user.username
        return self.auteur_nom