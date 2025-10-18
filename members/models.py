"""
Modèles pour l'application Members AMCD57
Gère les profils membres, fonctions bureau et types de membres
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import RegexValidator
from django.utils import timezone


# ============================================
# TYPE DE MEMBRE
# ============================================

class TypeMembre(models.Model):
    """
    Type de membre (Bureau, Actif, Honoraire, etc.)
    Définit le statut et les droits des membres
    """
    nom = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom du type"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les types avec un ordre plus petit apparaissent en premier"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Décocher pour désactiver ce type"
    )
    
    # Droits et privilèges
    peut_voter = models.BooleanField(
        default=True,
        verbose_name="Peut voter",
        help_text="Droit de vote aux assemblées"
    )
    
    acces_terrain = models.BooleanField(
        default=True,
        verbose_name="Accès terrain",
        help_text="Peut accéder au terrain de vol"
    )
    
    acces_espace_membre = models.BooleanField(
        default=True,
        verbose_name="Accès espace membre",
        help_text="Accès à l'espace membre du site"
    )
    
    class Meta:
        verbose_name = "Type de membre"
        verbose_name_plural = "Types de membres"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom
    
    @property
    def nombre_membres(self):
        """Compte le nombre de membres de ce type"""
        return self.profils.count()


# ============================================
# FONCTION BUREAU
# ============================================

class FonctionBureau(models.Model):
    """
    Fonction au sein du bureau du club
    (Président, Trésorier, Secrétaire, etc.)
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la fonction"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Responsabilités et missions de cette fonction"
    )
    
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Ordre d'affichage dans la liste du bureau"
    )
    
    email_contact = models.EmailField(
        blank=True,
        verbose_name="Email de contact",
        help_text="Email générique pour cette fonction (ex: president@amcd57.fr)"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    
    class Meta:
        verbose_name = "Fonction bureau"
        verbose_name_plural = "Fonctions bureau"
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom
    
    @property
    def membre_actuel(self):
        """Retourne le membre ayant actuellement cette fonction"""
        try:
            return self.profils.filter(
                fonction_active=True,
                user__is_active=True
            ).first()
        except:
            return None


# ============================================
# PROFIL MEMBRE
# ============================================

class ProfilMembre(models.Model):
    """
    Profil étendu d'un membre du club
    Extension du modèle User de Django (relation 1-1)
    """
    
    # Lien avec l'utilisateur Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profil',
        verbose_name="Utilisateur"
    )
    
    # Type de membre
    type_membre = models.ForeignKey(
        TypeMembre,
        on_delete=models.PROTECT,
        related_name='profils',
        verbose_name="Type de membre"
    )
    
    # Fonction bureau (optionnel)
    fonction_bureau = models.ForeignKey(
        FonctionBureau,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='profils',
        verbose_name="Fonction au bureau"
    )
    
    fonction_active = models.BooleanField(
        default=False,
        verbose_name="Fonction active",
        help_text="Cocher si le membre exerce actuellement sa fonction au bureau"
    )
    
    # Informations personnelles
    photo = models.ImageField(
        upload_to='members/photos/',
        null=True,
        blank=True,
        verbose_name="Photo de profil"
    )
    
    date_naissance = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de naissance"
    )
    
    telephone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'. 9 à 15 chiffres."
    )
    
    telephone = models.CharField(
        validators=[telephone_regex],
        max_length=17,
        blank=True,
        verbose_name="Téléphone"
    )
    
    telephone_portable = models.CharField(
        validators=[telephone_regex],
        max_length=17,
        blank=True,
        verbose_name="Téléphone portable"
    )
    
    # Adresse
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
    
    pays = models.CharField(
        max_length=100,
        default='France',
        verbose_name="Pays"
    )
    
    # Biographie et expérience
    bio = models.TextField(
        blank=True,
        verbose_name="Biographie",
        help_text="Présentation du membre"
    )
    
    experience_aeromodelisme = models.TextField(
        blank=True,
        verbose_name="Expérience en aéromodélisme",
        help_text="Années de pratique, spécialités, etc."
    )
    
    # Informations aéromodélisme
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]
    
    niveau = models.CharField(
        max_length=15,
        choices=NIVEAU_CHOICES,
        default='debutant',
        verbose_name="Niveau"
    )
    
    specialites = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Spécialités",
        help_text="Ex: Planeur, Thermique, Voltige, etc. (séparés par des virgules)"
    )
    
    avions_possedes = models.TextField(
        blank=True,
        verbose_name="Avions possédés",
        help_text="Liste des modèles possédés"
    )
    
    # Licences et assurances
    numero_licence_ufolep = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Numéro de licence UFOLEP",
        help_text="Union Française des Œuvres Laïques d'Éducation Physique"
    )
    
    date_validite_licence = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de validité de la licence"
    )
    
    assurance_valide = models.BooleanField(
        default=False,
        verbose_name="Assurance valide",
        help_text="L'assurance RC est-elle à jour ?"
    )
    
    # Adhésion au club
    date_adhesion = models.DateField(
        default=timezone.now,
        verbose_name="Date d'adhésion au club"
    )
    
    cotisation_a_jour = models.BooleanField(
        default=False,
        verbose_name="Cotisation à jour"
    )
    
    date_fin_cotisation = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin de cotisation"
    )
    
    # Préférences
    newsletter = models.BooleanField(
        default=True,
        verbose_name="Newsletter",
        help_text="Recevoir la newsletter du club"
    )
    
    notifications_evenements = models.BooleanField(
        default=True,
        verbose_name="Notifications événements",
        help_text="Recevoir les notifications d'événements"
    )
    
    profil_public = models.BooleanField(
        default=False,
        verbose_name="Profil public",
        help_text="Rendre le profil visible publiquement"
    )
    
    # Réseaux sociaux
    site_web = models.URLField(
        blank=True,
        verbose_name="Site web personnel"
    )
    
    youtube = models.URLField(
        blank=True,
        verbose_name="Chaîne YouTube"
    )
    
    facebook = models.URLField(
        blank=True,
        verbose_name="Profil Facebook"
    )
    
    instagram = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Instagram",
        help_text="Nom d'utilisateur Instagram (sans @)"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création du profil"
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )
    
    notes_admin = models.TextField(
        blank=True,
        verbose_name="Notes administratives",
        help_text="Notes internes (non visibles par le membre)"
    )
    
    class Meta:
        verbose_name = "Profil membre"
        verbose_name_plural = "Profils membres"
        ordering = ['user__last_name', 'user__first_name']
        indexes = [
            models.Index(fields=['type_membre']),
            models.Index(fields=['fonction_bureau']),
            models.Index(fields=['cotisation_a_jour']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.type_membre}"
    
    def get_absolute_url(self):
        """URL du profil"""
        return reverse('members:profil_detail', kwargs={'pk': self.pk})
    
    # Propriétés et méthodes utiles
    
    @property
    def nom_complet(self):
        """Retourne le nom complet du membre"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    @property
    def age(self):
        """Calcule l'âge du membre"""
        if self.date_naissance:
            today = timezone.now().date()
            age = today.year - self.date_naissance.year
            if today.month < self.date_naissance.month or \
               (today.month == self.date_naissance.month and today.day < self.date_naissance.day):
                age -= 1
            return age
        return None
    
    @property
    def est_membre_bureau(self):
        """Vérifie si le membre fait partie du bureau"""
        return self.fonction_bureau is not None and self.fonction_active
    
    @property
    def cotisation_expiree(self):
        """Vérifie si la cotisation est expirée"""
        if self.date_fin_cotisation:
            return timezone.now().date() > self.date_fin_cotisation
        return True
    
    @property
    def licence_expiree(self):
        """Vérifie si la licence FFAM est expirée"""
        if self.date_validite_licence:
            return timezone.now().date() > self.date_validite_licence
        return True
    
    @property
    def anciennete_annees(self):
        """Calcule l'ancienneté en années"""
        if self.date_adhesion:
            delta = timezone.now().date() - self.date_adhesion
            return delta.days // 365
        return 0
    
    @property
    def liste_specialites(self):
        """Retourne la liste des spécialités"""
        if self.specialites:
            return [s.strip() for s in self.specialites.split(',')]
        return []
    
    def peut_voter(self):
        """Vérifie si le membre peut voter"""
        return self.type_membre.peut_voter and self.cotisation_a_jour
    
    def peut_acceder_terrain(self):
        """Vérifie si le membre peut accéder au terrain"""
        return self.type_membre.acces_terrain and self.cotisation_a_jour and self.assurance_valide
    
    def renouveler_cotisation(self, duree_mois=12):
        """Renouvelle la cotisation pour une durée donnée"""
        from datetime import timedelta
        today = timezone.now().date()
        
        if self.date_fin_cotisation and self.date_fin_cotisation > today:
            # Prolonge à partir de la date de fin actuelle
            self.date_fin_cotisation = self.date_fin_cotisation + timedelta(days=duree_mois*30)
        else:
            # Nouvelle cotisation à partir d'aujourd'hui
            self.date_fin_cotisation = today + timedelta(days=duree_mois*30)
        
        self.cotisation_a_jour = True
        self.save()


# ============================================
# SIGNAL : Création automatique du profil
# ============================================

@receiver(post_save, sender=User)
def creer_profil_membre(sender, instance, created, **kwargs):
    """
    Signal Django : Crée automatiquement un ProfilMembre
    quand un User est créé
    """
    if created:
        # Récupère ou crée le type "Actif" par défaut
        type_actif, _ = TypeMembre.objects.get_or_create(
            nom='Actif',
            defaults={
                'description': 'Membre actif du club',
                'ordre': 2
            }
        )
        
        ProfilMembre.objects.create(
            user=instance,
            type_membre=type_actif
        )


@receiver(post_save, sender=User)
def sauvegarder_profil_membre(sender, instance, **kwargs):
    """
    Signal Django : Sauvegarde le profil quand le User est sauvegardé
    """
    if hasattr(instance, 'profil'):
        instance.profil.save()