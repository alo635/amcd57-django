from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Article, Categorie, Tag, Commentaire

User = get_user_model()


class CategorieModelTest(TestCase):
    """Tests pour le modèle Categorie"""

    def setUp(self):
        self.categorie = Categorie.objects.create(
            nom="Test Categorie",
            description="Description test"
        )

    def test_categorie_creation(self):
        """Test création d'une catégorie"""
        self.assertEqual(self.categorie.nom, "Test Categorie")
        self.assertEqual(self.categorie.slug, "test-categorie")

    def test_categorie_str(self):
        """Test représentation string"""
        self.assertEqual(str(self.categorie), "Test Categorie")

    def test_categorie_absolute_url(self):
        """Test génération URL"""
        expected_url = reverse('blog:categorie_detail', kwargs={'slug': self.categorie.slug})
        self.assertEqual(self.categorie.get_absolute_url(), expected_url)

    def test_nombre_articles_property(self):
        """Test comptage des articles publiés"""
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='password123'
        )

        # Créer 3 articles publiés
        for i in range(3):
            Article.objects.create(
                titre=f"Article {i}",
                contenu="Contenu test",
                categorie=self.categorie,
                auteur=user,
                statut='publie',
                date_publication=timezone.now()
            )

        # Créer 1 brouillon (ne doit pas être compté)
        Article.objects.create(
            titre="Brouillon",
            contenu="Contenu",
            categorie=self.categorie,
            auteur=user,
            statut='brouillon'
        )

        self.assertEqual(self.categorie.nombre_articles, 3)


class TagModelTest(TestCase):
    """Tests pour le modèle Tag"""

    def setUp(self):
        self.tag = Tag.objects.create(nom="Python")

    def test_tag_creation(self):
        """Test création d'un tag"""
        self.assertEqual(self.tag.nom, "Python")
        self.assertEqual(self.tag.slug, "python")

    def test_tag_str(self):
        """Test représentation string"""
        self.assertEqual(str(self.tag), "Python")


class ArticleModelTest(TestCase):
    """Tests pour le modèle Article"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='author',
            email='author@test.com',
            password='password123'
        )
        self.categorie = Categorie.objects.create(
            nom="Technique",
            description="Articles techniques"
        )
        self.tag1 = Tag.objects.create(nom="Django")
        self.tag2 = Tag.objects.create(nom="Python")

    def test_article_brouillon_creation(self):
        """Test création d'un article en brouillon"""
        article = Article.objects.create(
            titre="Mon article",
            contenu="Contenu de l'article",
            categorie=self.categorie,
            auteur=self.user,
            statut='brouillon'
        )

        self.assertEqual(article.titre, "Mon article")
        self.assertEqual(article.slug, "mon-article")
        self.assertEqual(article.statut, 'brouillon')
        self.assertIsNone(article.date_publication)

    def test_article_publie_date_publication(self):
        """Test que la date de publication est définie lors de la publication"""
        article = Article.objects.create(
            titre="Article publié",
            contenu="Contenu",
            categorie=self.categorie,
            auteur=self.user,
            statut='publie'
        )

        self.assertIsNotNone(article.date_publication)
        self.assertEqual(article.statut, 'publie')

    def test_article_extrait_auto_generation(self):
        """Test génération automatique de l'extrait"""
        long_content = "A" * 200  # Contenu de 200 caractères
        article = Article.objects.create(
            titre="Article",
            contenu=long_content,
            categorie=self.categorie,
            auteur=self.user,
            statut='publie'
        )

        # L'extrait doit être généré (150 premiers caractères + ...)
        self.assertTrue(len(article.extrait) <= 153)  # 150 + "..."

    def test_article_slug_uniqueness(self):
        """Test unicité du slug"""
        Article.objects.create(
            titre="Test",
            contenu="Contenu",
            categorie=self.categorie,
            auteur=self.user,
            statut='publie'
        )

        # Deuxième article avec même titre devrait avoir un slug différent
        article2 = Article.objects.create(
            titre="Test",
            contenu="Contenu 2",
            categorie=self.categorie,
            auteur=self.user,
            statut='publie'
        )

        self.assertNotEqual(article2.slug, "test")
        self.assertTrue(article2.slug.startswith("test-"))

    def test_article_tags_relationship(self):
        """Test relation ManyToMany avec les tags"""
        article = Article.objects.create(
            titre="Article avec tags",
            contenu="Contenu",
            categorie=self.categorie,
            auteur=self.user,
            statut='publie'
        )

        article.tags.add(self.tag1, self.tag2)

        self.assertEqual(article.tags.count(), 2)
        self.assertIn(self.tag1, article.tags.all())
        self.assertIn(self.tag2, article.tags.all())

    def test_article_str(self):
        """Test représentation string"""
        article = Article.objects.create(
            titre="Mon Article",
            contenu="Contenu",
            categorie=self.categorie,
            auteur=self.user
        )

        self.assertEqual(str(article), "Mon Article")

    def test_article_absolute_url(self):
        """Test génération URL"""
        article = Article.objects.create(
            titre="Test URL",
            contenu="Contenu",
            categorie=self.categorie,
            auteur=self.user
        )

        expected_url = reverse('blog:article_detail', kwargs={'slug': article.slug})
        self.assertEqual(article.get_absolute_url(), expected_url)


class CommentaireModelTest(TestCase):
    """Tests pour le modèle Commentaire"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='password123'
        )
        self.categorie = Categorie.objects.create(nom="Test")
        self.article = Article.objects.create(
            titre="Article de test",
            contenu="Contenu",
            categorie=self.categorie,
            auteur=self.user,
            statut='publie',
            date_publication=timezone.now()
        )

    def test_commentaire_creation_with_user(self):
        """Test création d'un commentaire par un utilisateur authentifié"""
        commentaire = Commentaire.objects.create(
            article=self.article,
            auteur_nom=self.user.email,
            auteur_email=self.user.email,
            contenu="Super article !"
        )

        self.assertEqual(commentaire.article, self.article)
        self.assertEqual(commentaire.auteur_nom, self.user.email)
        self.assertEqual(commentaire.auteur_email, self.user.email)
        self.assertFalse(commentaire.approuve)

    def test_commentaire_creation_visitor(self):
        """Test création d'un commentaire par un visiteur"""
        commentaire = Commentaire.objects.create(
            article=self.article,
            auteur_nom="Jean Dupont",
            auteur_email="jean@example.com",
            contenu="Commentaire de visiteur"
        )

        self.assertEqual(commentaire.auteur_nom, "Jean Dupont")
        self.assertEqual(commentaire.auteur_email, "jean@example.com")

    def test_commentaire_reply(self):
        """Test réponse à un commentaire"""
        commentaire_parent = Commentaire.objects.create(
            article=self.article,
            auteur_nom=self.user.email,
            auteur_email=self.user.email,
            contenu="Commentaire parent",
            approuve=True
        )

        commentaire_enfant = Commentaire.objects.create(
            article=self.article,
            auteur_nom=self.user.email,
            auteur_email=self.user.email,
            contenu="Réponse",
            parent=commentaire_parent,
            approuve=True
        )

        self.assertEqual(commentaire_enfant.parent, commentaire_parent)
        self.assertIn(commentaire_enfant, commentaire_parent.reponses.all())

    def test_commentaire_str(self):
        """Test représentation string"""
        commentaire = Commentaire.objects.create(
            article=self.article,
            auteur_nom=self.user.email,
            auteur_email=self.user.email,
            contenu="Test commentaire"
        )

        expected_str = f"Commentaire de {self.user.email} sur {self.article.titre}"
        self.assertEqual(str(commentaire), expected_str)


class ArticleViewsTest(TestCase):
    """Tests pour les vues de l'application Blog"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='password123'
        )
        self.categorie = Categorie.objects.create(nom="Test")

        # Créer plusieurs articles publiés
        for i in range(5):
            Article.objects.create(
                titre=f"Article {i}",
                contenu=f"Contenu {i}",
                categorie=self.categorie,
                auteur=self.user,
                statut='publie',
                date_publication=timezone.now() - timedelta(days=i)
            )

        # Créer un brouillon
        self.brouillon = Article.objects.create(
            titre="Brouillon",
            contenu="Contenu brouillon",
            categorie=self.categorie,
            auteur=self.user,
            statut='brouillon'
        )

    def test_article_list_view(self):
        """Test de la vue liste des articles"""
        response = self.client.get(reverse('blog:article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')

        # Doit contenir 5 articles publiés (pas le brouillon)
        self.assertEqual(len(response.context['articles']), 5)

    def test_article_list_pagination(self):
        """Test pagination de la liste des articles"""
        # Créer 15 articles supplémentaires (total = 20)
        for i in range(15):
            Article.objects.create(
                titre=f"Article page 2 - {i}",
                contenu=f"Contenu {i}",
                categorie=self.categorie,
                auteur=self.user,
                statut='publie',
                date_publication=timezone.now()
            )

        # Page 1 devrait avoir 9 articles (pagination = 9 par page)
        response = self.client.get(reverse('blog:article_list'))
        self.assertEqual(len(response.context['articles']), 9)

        # Page 2 devrait avoir 9 articles
        response = self.client.get(reverse('blog:article_list') + '?page=2')
        self.assertEqual(len(response.context['articles']), 9)

        # Page 3 devrait avoir 2 articles (20 total - 9 - 9 = 2)
        response = self.client.get(reverse('blog:article_list') + '?page=3')
        self.assertEqual(len(response.context['articles']), 2)

    def test_article_detail_view_published(self):
        """Test vue détail d'un article publié"""
        article = Article.objects.filter(statut='publie').first()
        response = self.client.get(reverse('blog:article_detail', kwargs={'slug': article.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_detail.html')
        self.assertEqual(response.context['article'], article)

    def test_article_detail_view_draft_404(self):
        """Test qu'un brouillon retourne 404"""
        response = self.client.get(reverse('blog:article_detail', kwargs={'slug': self.brouillon.slug}))

        self.assertEqual(response.status_code, 404)

    def test_article_detail_increments_views(self):
        """Test que la vue incrémente le compteur de vues"""
        article = Article.objects.filter(statut='publie').first()
        initial_views = article.vues

        self.client.get(reverse('blog:article_detail', kwargs={'slug': article.slug}))

        article.refresh_from_db()
        self.assertEqual(article.vues, initial_views + 1)

    def test_categorie_detail_view(self):
        """Test vue détail d'une catégorie"""
        response = self.client.get(reverse('blog:categorie_detail', kwargs={'slug': self.categorie.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/categorie_detail.html')
        self.assertEqual(response.context['categorie'], self.categorie)

    def test_search_view(self):
        """Test vue recherche"""
        response = self.client.get(reverse('blog:article_search') + '?q=Article')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_search.html')
        # Devrait trouver les articles contenant "Article" dans le titre
        self.assertGreater(len(response.context['articles']), 0)

    def test_search_view_no_results(self):
        """Test recherche sans résultats"""
        response = self.client.get(reverse('blog:article_search') + '?q=Inexistant')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), 0)
