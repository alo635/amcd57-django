from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .models import TypeMembre, FonctionBureau, ProfilMembre

User = get_user_model()


class TypeMembreModelTest(TestCase):
    """Tests pour le modèle TypeMembre"""

    def setUp(self):
        self.type_membre = TypeMembre.objects.create(
            nom="Actif",
            description="Membre actif du club",
            ordre=1,
            peut_voter=True,
            acces_terrain=True,
            acces_espace_membre=True
        )

    def test_type_membre_creation(self):
        """Test création d'un type de membre"""
        self.assertEqual(self.type_membre.nom, "Actif")
        self.assertTrue(self.type_membre.actif)
        self.assertTrue(self.type_membre.peut_voter)
        self.assertTrue(self.type_membre.acces_terrain)

    def test_type_membre_str(self):
        """Test représentation string"""
        self.assertEqual(str(self.type_membre), "Actif")

    def test_nombre_membres_property(self):
        """Test comptage des membres d'un type"""
        # Créer des profils
        for i in range(3):
            user = User.objects.create_user(
                username=f'user{i}',
                email=f'user{i}@test.com',
                password='password123'
            )
            ProfilMembre.objects.create(
                user=user,
                type_membre=self.type_membre,
                date_naissance=date(1990, 1, 1)
            )

        self.assertEqual(self.type_membre.nombre_membres, 3)


class FonctionBureauModelTest(TestCase):
    """Tests pour le modèle FonctionBureau"""

    def setUp(self):
        self.fonction = FonctionBureau.objects.create(
            nom="Président",
            description="Responsable du club",
            ordre=1
        )

    def test_fonction_bureau_creation(self):
        """Test création d'une fonction bureau"""
        self.assertEqual(self.fonction.nom, "Président")
        self.assertEqual(self.fonction.ordre, 1)

    def test_fonction_bureau_str(self):
        """Test représentation string"""
        self.assertEqual(str(self.fonction), "Président")


class ProfilMembreModelTest(TestCase):
    """Tests pour le modèle ProfilMembre"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='password123',
            first_name='Jean',
            last_name='Dupont'
        )
        self.type_membre = TypeMembre.objects.create(
            nom="Actif",
            peut_voter=True,
            acces_terrain=True
        )
        self.fonction = FonctionBureau.objects.create(
            nom="Secrétaire",
            ordre=2
        )
        self.profil = ProfilMembre.objects.create(
            user=self.user,
            type_membre=self.type_membre,
            date_naissance=date(1990, 5, 15),
            telephone="0612345678",
            adresse="123 rue Test",
            code_postal="57000",
            ville="Metz"
        )

    def test_profil_membre_creation(self):
        """Test création d'un profil membre"""
        self.assertEqual(self.profil.user, self.user)
        self.assertEqual(self.profil.type_membre, self.type_membre)
        self.assertEqual(self.profil.telephone, "0612345678")

    def test_nom_complet_property(self):
        """Test propriété nom_complet"""
        self.assertEqual(self.profil.nom_complet, "Jean Dupont")

    def test_age_property(self):
        """Test calcul de l'âge"""
        # L'âge devrait être environ 34-35 ans (2025 - 1990)
        self.assertGreaterEqual(self.profil.age, 34)
        self.assertLessEqual(self.profil.age, 35)

    def test_est_membre_bureau_property(self):
        """Test vérification membre du bureau"""
        # Sans fonction
        self.assertFalse(self.profil.est_membre_bureau)

        # Avec fonction - note: doit être actif
        self.profil.fonction_bureau = self.fonction
        self.profil.fonction_active = True
        self.profil.save()
        self.assertTrue(self.profil.est_membre_bureau)

    def test_profil_str(self):
        """Test représentation string"""
        expected_str = f"{self.user.get_full_name()} - {self.type_membre.nom}"
        self.assertEqual(str(self.profil), expected_str)


class MembersViewsTest(TestCase):
    """Tests pour les vues de l'application Members"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='password123'
        )
        self.type_membre = TypeMembre.objects.create(
            nom="Actif",
            acces_espace_membre=True
        )
        self.profil = ProfilMembre.objects.create(
            user=self.user,
            type_membre=self.type_membre,
            date_naissance=date(1990, 1, 1)
        )

    def test_dashboard_requires_login(self):
        """Test que le dashboard nécessite une connexion"""
        response = self.client.get(reverse('members:dashboard'))

        # Devrait rediriger vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_dashboard_authenticated(self):
        """Test accès au dashboard pour utilisateur authentifié"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('members:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members/dashboard.html')

    def test_bureau_list_view(self):
        """Test de la vue liste du bureau"""
        # Créer un membre du bureau
        fonction = FonctionBureau.objects.create(nom="Président", ordre=1)
        self.profil.fonction_bureau = fonction
        self.profil.save()

        response = self.client.get(reverse('members:bureau'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members/bureau.html')
