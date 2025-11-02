from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class PageView(models.Model):
    """
    Modèle pour tracker les pages vues.
    Enregistre chaque visite de page pour analyse ultérieure.
    """
    url = models.CharField(
        max_length=500,
        verbose_name="URL visitée"
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Utilisateur",
        help_text="Utilisateur connecté (si authentifié)"
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="Adresse IP"
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="User Agent",
        help_text="Navigateur et système d'exploitation"
    )
    referer = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Référent",
        help_text="Page d'origine de la visite"
    )
    session_key = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Clé de session"
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name="Date et heure"
    )
    response_time = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Temps de réponse (ms)",
        help_text="Temps de traitement de la requête en millisecondes"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Page vue"
        verbose_name_plural = "Pages vues"
        indexes = [
            models.Index(fields=['timestamp', 'url']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.url} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    def get_short_url(self):
        """Retourne une version raccourcie de l'URL"""
        if len(self.url) > 50:
            return self.url[:47] + '...'
        return self.url
