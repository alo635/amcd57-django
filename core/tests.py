from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import ContactMessage


class ContactMessageModelTest(TestCase):
    """Tests pour le modèle ContactMessage"""

    def setUp(self):
        self.message = ContactMessage.objects.create(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@example.com",
            telephone="0612345678",
            sujet="info",
            message="Bonjour, je souhaite des informations sur le club."
        )

    def test_contact_message_creation(self):
        """Test création d'un message de contact"""
        self.assertEqual(self.message.nom, "Dupont")
        self.assertEqual(self.message.prenom, "Jean")
        self.assertEqual(self.message.email, "jean.dupont@example.com")
        self.assertEqual(self.message.sujet, "info")
        self.assertEqual(self.message.statut, "nouveau")
        self.assertFalse(self.message.lu)
        self.assertFalse(self.message.repondu)

    def test_nom_complet_property_with_prenom(self):
        """Test nom complet avec prénom"""
        self.assertEqual(self.message.nom_complet, "Jean Dupont")

    def test_nom_complet_property_without_prenom(self):
        """Test nom complet sans prénom"""
        message_sans_prenom = ContactMessage.objects.create(
            nom="Martin",
            email="martin@example.com",
            sujet="adhesion",
            message="Je souhaite adhérer"
        )
        self.assertEqual(message_sans_prenom.nom_complet, "Martin")

    def test_est_nouveau_property(self):
        """Test propriété est_nouveau"""
        # Message nouveau et non lu
        self.assertTrue(self.message.est_nouveau)

        # Message lu
        self.message.lu = True
        self.message.save()
        self.assertFalse(self.message.est_nouveau)

        # Message traité
        message_traite = ContactMessage.objects.create(
            nom="Test",
            email="test@example.com",
            sujet="info",
            message="Test",
            statut="traite"
        )
        self.assertFalse(message_traite.est_nouveau)

    def test_age_message_property(self):
        """Test calcul de l'âge du message"""
        # Message récent (aujourd'hui)
        self.assertEqual(self.message.age_message, 0)

        # Message ancien (simuler avec un message créé il y a 5 jours)
        old_message = ContactMessage.objects.create(
            nom="Test",
            email="test@example.com",
            sujet="info",
            message="Test"
        )
        old_message.date_envoi = timezone.now() - timedelta(days=5)
        old_message.save()
        self.assertEqual(old_message.age_message, 5)

    def test_marquer_lu_method(self):
        """Test méthode marquer_lu"""
        self.assertFalse(self.message.lu)
        self.message.marquer_lu()
        self.assertTrue(self.message.lu)

    def test_marquer_traite_method(self):
        """Test méthode marquer_traite"""
        self.assertEqual(self.message.statut, "nouveau")
        self.assertIsNone(self.message.date_traitement)

        self.message.marquer_traite()

        self.assertEqual(self.message.statut, "traite")
        self.assertIsNotNone(self.message.date_traitement)

    def test_marquer_repondu_method(self):
        """Test méthode marquer_repondu"""
        self.assertFalse(self.message.repondu)
        self.assertEqual(self.message.statut, "nouveau")
        self.assertIsNone(self.message.date_reponse)

        self.message.marquer_repondu()

        self.assertTrue(self.message.repondu)
        self.assertEqual(self.message.statut, "en_cours")
        self.assertIsNotNone(self.message.date_reponse)

    def test_contact_message_str(self):
        """Test représentation string"""
        date_str = self.message.date_envoi.strftime('%d/%m/%Y')
        expected_str = f"Jean Dupont - Demande d'information ({date_str})"
        self.assertEqual(str(self.message), expected_str)


class CoreViewsTest(TestCase):
    """Tests pour les vues de l'application Core"""

    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        """Test de la page d'accueil"""
        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')

    def test_about_view(self):
        """Test de la page À propos"""
        response = self.client.get(reverse('core:about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_contact_view_get(self):
        """Test affichage du formulaire de contact"""
        response = self.client.get(reverse('core:contact'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_contact_view_post_valid(self):
        """Test soumission valide du formulaire de contact"""
        data = {
            'nom': 'Test',
            'prenom': 'User',
            'email': 'test@example.com',
            'telephone': '0612345678',
            'sujet': 'info',
            'message': 'Message de test'
        }

        response = self.client.post(reverse('core:contact'), data)

        # Devrait créer le message et rediriger
        self.assertEqual(ContactMessage.objects.count(), 1)
        message = ContactMessage.objects.first()
        self.assertEqual(message.nom, 'Test')
        self.assertEqual(message.email, 'test@example.com')

    def test_legal_view(self):
        """Test de la page Mentions légales"""
        response = self.client.get(reverse('core:mentions_legales'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/mentions_legales.html')

    def test_privacy_view(self):
        """Test de la page Politique de confidentialité"""
        response = self.client.get(reverse('core:politique_confidentialite'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/politique_confidentialite.html')

    def test_terms_view(self):
        """Test de la page Conditions d'utilisation"""
        response = self.client.get(reverse('core:cgu'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/cgu.html')
