"""
Modèles pour l'application Events AMCD57
Gère les événements, lieux, types d'événements et inscriptions
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError


# ============================================
# TYPE D'ÉVÉNEMENT
# ============================================

class TypeEvenement(models.Model):
    """
    Type d'événement (Réunion, Sortie, Vol, Compétition, etc.)
    Permet d'organiser et filtrer les événements
    """
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom du type"
    )
    
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Slug"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    couleur = models.CharField(
        max_length=7,
        default='#3B82F6',
        verbose_name="Couleur",
        help_text="Code couleur hexadécimal (ex: #3B82F6)"
    )
    
    icone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icône",
        help_text="Nom de l'icône (ex: calendar, plane, users)"
    )
    
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Décocher pour désactiver ce type d'événement"
    )
    
    class Meta:
        verbose_name = "Type d'événement"
        verbose_name_plural = "Types d'événements"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    @property
    def nombre_evenements(self):
        """Compte le nombre d'événements de ce type"""
        return self.evenements.count()
    
    @property
    def prochains_evenements(self):
        """Retourne les prochains événements de ce type"""
        return self.evenements.filter(
            date_debut__gte=timezone.now()
        ).order_by('date_debut')[:5]


# ============================================
# LIEU
# ============================================

class Lieu(models.Model):
    """
    Lieu où se déroule un événement
    (Terrain de vol, salle de réunion, etc.)
    """
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du lieu"
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug"
    )
    
    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse"
    )
    
    code_postal = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Code postal"
    )
    
    ville = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ville"
    )
    
    # Coordonnées GPS pour affichage sur carte
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitude",
        help_text="Ex: 49.158889"
    )
    
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Longitude",
        help_text="Ex: 5.883333"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    image = models.ImageField(
        upload_to='events/lieux/',
        null=True,
        blank=True,
        verbose_name="Photo du lieu"
    )
    
    capacite = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Capacité",
        help_text="Nombre maximum de personnes"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    
    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"
        ordering = ['nom']
    
    def __str__(self):
        if self.ville:
            return f"{self.nom} ({self.ville})"
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('events:lieu_detail', kwargs={'slug': self.slug})
    
    @property
    def adresse_complete(self):
        """Retourne l'adresse complète formatée"""
        parts = [self.adresse, self.code_postal, self.ville]
        return ', '.join(filter(None, parts))
    
    @property
    def a_coordonnees_gps(self):
        """Vérifie si le lieu a des coordonnées GPS"""
        return self.latitude is not None and self.longitude is not None


# ============================================
# ÉVÉNEMENT
# ============================================

class Evenement(models.Model):
    """
    Événement du club (réunion, sortie, vol, compétition, etc.)
    """
    
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
    ]
    
    # Informations principales
    titre = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug"
    )
    
    description = models.TextField(
        verbose_name="Description"
    )
    
    description_courte = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Description courte",
        help_text="Résumé pour le calendrier"
    )
    
    # Classification
    type_evenement = models.ForeignKey(
        TypeEvenement,
        on_delete=models.PROTECT,
        related_name='evenements',
        verbose_name="Type d'événement"
    )
    
    # Lieu
    lieu = models.ForeignKey(
        Lieu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evenements',
        verbose_name="Lieu"
    )
    
    lieu_details = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Précisions sur le lieu",
        help_text="Ex: Salle 3, Piste Nord, etc."
    )
    
    # Dates et horaires
    date_debut = models.DateTimeField(
        verbose_name="Date et heure de début"
    )
    
    date_fin = models.DateTimeField(
        verbose_name="Date et heure de fin"
    )
    
    journee_complete = models.BooleanField(
        default=False,
        verbose_name="Journée complète",
        help_text="Cocher si l'événement dure toute la journée"
    )
    
    # Organisateur
    organisateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='evenements_organises',
        verbose_name="Organisateur"
    )
    
    # Statut
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='planifie',
        verbose_name="Statut"
    )
    
    # Inscriptions
    inscription_requise = models.BooleanField(
        default=False,
        verbose_name="Inscription requise"
    )
    
    places_limitees = models.BooleanField(
        default=False,
        verbose_name="Places limitées"
    )
    
    nombre_places = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nombre de places",
        help_text="Laisser vide si illimité"
    )
    
    date_limite_inscription = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date limite d'inscription"
    )
    
    # Visibilité
    public = models.BooleanField(
        default=True,
        verbose_name="Public",
        help_text="Visible par tous (même non-membres)"
    )
    
    membres_seulement = models.BooleanField(
        default=False,
        verbose_name="Membres uniquement",
        help_text="Visible uniquement par les membres connectés"
    )
    
    # Médias
    image = models.ImageField(
        upload_to='events/evenements/%Y/%m/',
        null=True,
        blank=True,
        verbose_name="Image"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    vues = models.IntegerField(
        default=0,
        verbose_name="Nombre de vues",
        editable=False
    )
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date_debut']
        indexes = [
            models.Index(fields=['date_debut']),
            models.Index(fields=['statut']),
            models.Index(fields=['type_evenement']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.date_debut.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        # Auto-génération du slug
        if not self.slug:
            self.slug = slugify(self.titre)
            original_slug = self.slug
            counter = 1
            while Evenement.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Génère description courte si vide
        if not self.description_courte and self.description:
            self.description_courte = self.description[:150]
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validation personnalisée"""
        # Vérifie que la date de fin est après la date de début
        if self.date_fin and self.date_debut and self.date_fin <= self.date_debut:
            raise ValidationError({
                'date_fin': 'La date de fin doit être après la date de début.'
            })
        
        # Vérifie que la date limite d'inscription est avant la date de début
        if self.date_limite_inscription and self.date_limite_inscription >= self.date_debut:
            raise ValidationError({
                'date_limite_inscription': 'La date limite d\'inscription doit être avant le début de l\'événement.'
            })
    
    def get_absolute_url(self):
        return reverse('events:evenement_detail', kwargs={'slug': self.slug})
    
    # Propriétés et méthodes utiles
    
    @property
    def est_passe(self):
        """Vérifie si l'événement est passé"""
        return self.date_fin < timezone.now()
    
    @property
    def est_en_cours(self):
        """Vérifie si l'événement est en cours"""
        now = timezone.now()
        return self.date_debut <= now <= self.date_fin
    
    @property
    def est_futur(self):
        """Vérifie si l'événement est à venir"""
        return self.date_debut > timezone.now()
    
    @property
    def est_annule(self):
        """Vérifie si l'événement est annulé"""
        return self.statut == 'annule'
    
    @property
    def inscriptions_ouvertes(self):
        """Vérifie si les inscriptions sont ouvertes"""
        if not self.inscription_requise:
            return False
        
        now = timezone.now()
        
        # Vérifie la date limite
        if self.date_limite_inscription and now > self.date_limite_inscription:
            return False
        
        # Vérifie si l'événement est passé
        if self.est_passe:
            return False
        
        # Vérifie les places disponibles
        if self.places_limitees and self.places_restantes <= 0:
            return False
        
        return True
    
    @property
    def nombre_inscrits(self):
        """Compte le nombre d'inscrits"""
        return self.inscriptions.filter(statut='confirme').count()
    
    @property
    def places_restantes(self):
        """Calcule le nombre de places restantes"""
        if not self.places_limitees or not self.nombre_places:
            return None
        return self.nombre_places - self.nombre_inscrits
    
    @property
    def est_complet(self):
        """Vérifie si l'événement est complet"""
        if not self.places_limitees:
            return False
        places = self.places_restantes
        return places is not None and places <= 0
    
    @property
    def duree(self):
        """Retourne la durée de l'événement"""
        return self.date_fin - self.date_debut
    
    def incrementer_vues(self):
        """Incrémente le compteur de vues"""
        self.vues += 1
        self.save(update_fields=['vues'])
    
    def peut_sinscrire(self, user):
        """Vérifie si un utilisateur peut s'inscrire"""
        if not self.inscription_requise:
            return False
        
        if not self.inscriptions_ouvertes:
            return False
        
        # Vérifie si déjà inscrit
        if self.inscriptions.filter(participant=user).exists():
            return False
        
        return True


# ============================================
# INSCRIPTION
# ============================================

class Inscription(models.Model):
    """
    Inscription d'un participant à un événement
    """
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('liste_attente', 'Liste d\'attente'),
    ]
    
    evenement = models.ForeignKey(
        Evenement,
        on_delete=models.CASCADE,
        related_name='inscriptions',
        verbose_name="Événement"
    )
    
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inscriptions_evenements',
        verbose_name="Participant"
    )
    
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    
    statut = models.CharField(
        max_length=15,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name="Statut"
    )
    
    nombre_accompagnants = models.IntegerField(
        default=0,
        verbose_name="Nombre d'accompagnants",
        help_text="Personnes accompagnant le participant"
    )
    
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire",
        help_text="Message ou demande particulière"
    )
    
    # Présence
    present = models.BooleanField(
        default=False,
        verbose_name="Présent",
        help_text="Cocher après l'événement si le participant était présent"
    )
    
    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        ordering = ['date_inscription']
        unique_together = ['evenement', 'participant']  # Empêche les doublons
        indexes = [
            models.Index(fields=['evenement', 'statut']),
        ]
    
    def __str__(self):
        return f"{self.participant.username} - {self.evenement.titre}"
    
    def clean(self):
        """Validation personnalisée"""
        # Vérifie que l'événement accepte les inscriptions
        if not self.evenement.inscription_requise:
            raise ValidationError("Cet événement ne nécessite pas d'inscription.")
        
        # Vérifie que les inscriptions sont ouvertes
        if not self.evenement.inscriptions_ouvertes and not self.pk:
            raise ValidationError("Les inscriptions sont fermées pour cet événement.")
    
    def confirmer(self):
        """Confirme l'inscription"""
        self.statut = 'confirme'
        self.save()
    
    def annuler(self):
        """Annule l'inscription"""
        self.statut = 'annule'
        self.save()
    
    def mettre_en_liste_attente(self):
        """Met l'inscription en liste d'attente"""
        self.statut = 'liste_attente'
        self.save()