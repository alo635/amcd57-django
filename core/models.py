"""
Modèles pour l'application Core AMCD57
Gère les fonctionnalités transversales (contact, etc.)
"""

from django.db import models
from django.utils import timezone


# ============================================
# MESSAGE DE CONTACT
# ============================================

class ContactMessage(models.Model):
    """
    Message envoyé via le formulaire de contact
    """
    
    STATUT_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('en_cours', 'En cours de traitement'),
        ('traite', 'Traité'),
        ('archive', 'Archivé'),
    ]
    
    SUJET_CHOICES = [
        ('info', 'Demande d\'information'),
        ('adhesion', 'Adhésion au club'),
        ('evenement', 'Question sur un événement'),
        ('technique', 'Question technique'),
        ('partenariat', 'Proposition de partenariat'),
        ('autre', 'Autre'),
    ]
    
    # Informations du contact
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom"
    )
    
    prenom = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Prénom"
    )
    
    email = models.EmailField(
        verbose_name="Email"
    )
    
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone"
    )
    
    # Message
    sujet = models.CharField(
        max_length=20,
        choices=SUJET_CHOICES,
        default='info',
        verbose_name="Sujet"
    )
    
    message = models.TextField(
        verbose_name="Message"
    )
    
    # Métadonnées
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP",
        help_text="Adresse IP de l'expéditeur"
    )
    
    # Gestion
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default='nouveau',
        verbose_name="Statut"
    )
    
    date_traitement = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de traitement"
    )
    
    lu = models.BooleanField(
        default=False,
        verbose_name="Lu"
    )
    
    # Réponse
    reponse = models.TextField(
        blank=True,
        verbose_name="Réponse",
        help_text="Réponse apportée au message (usage interne)"
    )
    
    repondu = models.BooleanField(
        default=False,
        verbose_name="Répondu"
    )
    
    date_reponse = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de réponse"
    )
    
    # Notes internes
    notes = models.TextField(
        blank=True,
        verbose_name="Notes internes",
        help_text="Notes administratives (non visibles par le contact)"
    )
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']
        indexes = [
            models.Index(fields=['statut', 'lu']),
            models.Index(fields=['-date_envoi']),
        ]
    
    def __str__(self):
        return f"{self.nom_complet} - {self.get_sujet_display()} ({self.date_envoi.strftime('%d/%m/%Y')})"
    
    @property
    def nom_complet(self):
        """Retourne le nom complet"""
        if self.prenom:
            return f"{self.prenom} {self.nom}"
        return self.nom
    
    @property
    def est_nouveau(self):
        """Vérifie si le message est nouveau (non lu)"""
        return self.statut == 'nouveau' and not self.lu
    
    @property
    def age_message(self):
        """Calcule l'âge du message en jours"""
        delta = timezone.now() - self.date_envoi
        return delta.days
    
    def marquer_lu(self):
        """Marque le message comme lu"""
        self.lu = True
        self.save(update_fields=['lu'])
    
    def marquer_traite(self):
        """Marque le message comme traité"""
        self.statut = 'traite'
        self.date_traitement = timezone.now()
        self.save(update_fields=['statut', 'date_traitement'])
    
    def marquer_repondu(self):
        """Marque le message comme répondu"""
        self.repondu = True
        self.date_reponse = timezone.now()
        if self.statut == 'nouveau':
            self.statut = 'en_cours'
        self.save(update_fields=['repondu', 'date_reponse', 'statut'])