#!/usr/bin/env python
"""
Script de migration des articles WordPress vers Django AMCD57

Ce script peut importer des articles depuis :
1. Export WordPress XML
2. Fichier JSON
3. Fichier CSV

Usage:
    python manage.py shell < migration_wordpress/scripts/import_articles.py

    Ou dans le shell Django :
    exec(open('migration_wordpress/scripts/import_articles.py').read())
"""

import os
import sys
import json
import csv
from datetime import datetime
from pathlib import Path
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from blog.models import Article, Categorie, Tag

User = get_user_model()


class WordPressImporter:
    """Classe pour gérer l'import d'articles WordPress"""

    def __init__(self, default_author_email='admin@amcd57.fr'):
        """
        Initialise l'importeur

        Args:
            default_author_email: Email de l'auteur par défaut si non spécifié
        """
        self.default_author_email = default_author_email
        self.stats = {
            'articles_created': 0,
            'articles_updated': 0,
            'articles_skipped': 0,
            'categories_created': 0,
            'tags_created': 0,
            'errors': []
        }

    def get_or_create_author(self, email=None, username=None):
        """Récupère ou crée un auteur"""
        email = email or self.default_author_email
        username = username or email.split('@')[0]

        try:
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            # Vérifie si le username existe déjà
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Crée un utilisateur si inexistant
            user = User.objects.create_user(
                email=email,
                username=username,
                is_active=True
            )
            print(f"✅ Utilisateur créé : {email} (username: {username})")
            return user

    def get_or_create_categorie(self, nom, slug=None, description=''):
        """Récupère ou crée une catégorie"""
        slug = slug or slugify(nom)

        categorie, created = Categorie.objects.get_or_create(
            slug=slug,
            defaults={
                'nom': nom,
                'description': description
            }
        )

        if created:
            self.stats['categories_created'] += 1
            print(f"✅ Catégorie créée : {nom}")

        return categorie

    def get_or_create_tag(self, nom, slug=None):
        """Récupère ou crée un tag"""
        slug = slug or slugify(nom)

        tag, created = Tag.objects.get_or_create(
            slug=slug,
            defaults={'nom': nom}
        )

        if created:
            self.stats['tags_created'] += 1
            print(f"✅ Tag créé : {nom}")

        return tag

    def import_from_json(self, json_file_path):
        """
        Importe des articles depuis un fichier JSON

        Format attendu :
        {
            "articles": [
                {
                    "titre": "Titre de l'article",
                    "contenu": "Contenu HTML...",
                    "extrait": "Résumé court",
                    "categorie": "Club",
                    "tags": ["tag1", "tag2"],
                    "date_publication": "2024-10-01 10:00:00",
                    "auteur_email": "auteur@amcd57.fr",
                    "statut": "publie",
                    "image": "chemin/vers/image.jpg",
                    "meta_description": "Description SEO"
                }
            ]
        }
        """
        print(f"\n📥 Import depuis JSON : {json_file_path}")

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé : {json_file_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON : {e}")
            return False

        articles_data = data.get('articles', [])
        print(f"📊 {len(articles_data)} article(s) trouvé(s)\n")

        for idx, article_data in enumerate(articles_data, 1):
            print(f"\n[{idx}/{len(articles_data)}] Traitement : {article_data.get('titre', 'Sans titre')}")
            self.import_article(article_data)

        self.print_stats()
        return True

    def import_from_csv(self, csv_file_path):
        """
        Importe des articles depuis un fichier CSV

        Colonnes attendues :
        titre,contenu,extrait,categorie,tags,date_publication,auteur_email,statut,image,meta_description
        """
        print(f"\n📥 Import depuis CSV : {csv_file_path}")

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                articles_data = list(reader)
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé : {csv_file_path}")
            return False

        print(f"📊 {len(articles_data)} article(s) trouvé(s)\n")

        for idx, article_data in enumerate(articles_data, 1):
            # Convertir les tags depuis string vers liste
            if 'tags' in article_data and article_data['tags']:
                article_data['tags'] = [t.strip() for t in article_data['tags'].split(',')]
            else:
                article_data['tags'] = []

            print(f"\n[{idx}/{len(articles_data)}] Traitement : {article_data.get('titre', 'Sans titre')}")
            self.import_article(article_data)

        self.print_stats()
        return True

    def import_article(self, data):
        """Importe un article individuel"""
        try:
            # Récupère ou crée l'auteur
            auteur = self.get_or_create_author(
                email=data.get('auteur_email'),
                username=data.get('auteur_username')
            )

            # Récupère ou crée la catégorie
            categorie = None
            if data.get('categorie'):
                categorie = self.get_or_create_categorie(data['categorie'])

            # Parse la date de publication
            date_publication = None
            if data.get('date_publication'):
                try:
                    date_publication = datetime.strptime(
                        data['date_publication'],
                        '%Y-%m-%d %H:%M:%S'
                    )
                    date_publication = timezone.make_aware(date_publication)
                except ValueError:
                    # Essaie un autre format
                    try:
                        date_publication = datetime.strptime(
                            data['date_publication'],
                            '%Y-%m-%d'
                        )
                        date_publication = timezone.make_aware(date_publication)
                    except ValueError:
                        print(f"⚠️  Format de date invalide, utilise la date actuelle")
                        date_publication = timezone.now()

            # Crée ou met à jour l'article
            slug = slugify(data['titre'])

            # Vérifie si l'article existe déjà
            existing_article = Article.objects.filter(slug=slug).first()

            if existing_article:
                print(f"⚠️  Article existant, mise à jour : {data['titre']}")
                article = existing_article
                self.stats['articles_updated'] += 1
            else:
                article = Article()
                self.stats['articles_created'] += 1

            # Met à jour les champs
            article.titre = data['titre']
            article.slug = slug
            article.contenu = data.get('contenu', '')
            article.extrait = data.get('extrait', '')
            article.auteur = auteur
            article.categorie = categorie
            article.statut = data.get('statut', 'publie')
            article.meta_description = data.get('meta_description', '')

            if date_publication:
                article.date_publication = date_publication

            # Gère l'image (si fournie)
            if data.get('image'):
                # TODO: Copier l'image depuis migration_wordpress/images/
                pass

            article.save()

            # Ajoute les tags
            if data.get('tags'):
                for tag_name in data['tags']:
                    tag = self.get_or_create_tag(tag_name)
                    article.tags.add(tag)

            print(f"✅ Article importé : {article.titre} (slug: {article.slug})")

        except Exception as e:
            error_msg = f"Erreur lors de l'import de '{data.get('titre', 'Sans titre')}': {str(e)}"
            print(f"❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            self.stats['articles_skipped'] += 1

    def print_stats(self):
        """Affiche les statistiques d'import"""
        print("\n" + "="*60)
        print("📊 STATISTIQUES D'IMPORT")
        print("="*60)
        print(f"Articles créés       : {self.stats['articles_created']}")
        print(f"Articles mis à jour  : {self.stats['articles_updated']}")
        print(f"Articles ignorés     : {self.stats['articles_skipped']}")
        print(f"Catégories créées    : {self.stats['categories_created']}")
        print(f"Tags créés           : {self.stats['tags_created']}")
        print(f"Erreurs              : {len(self.stats['errors'])}")

        if self.stats['errors']:
            print("\n❌ ERREURS RENCONTRÉES :")
            for error in self.stats['errors']:
                print(f"  - {error}")

        print("="*60 + "\n")


# ============================================================================
# EXEMPLE D'UTILISATION
# ============================================================================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  SCRIPT DE MIGRATION WORDPRESS → DJANGO AMCD57               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Initialise l'importeur
    importer = WordPressImporter(default_author_email='admin@amcd57.fr')

    # Chemins des fichiers
    # Détecte si on est appelé depuis le shell Django ou directement
    if __file__:
        base_path = Path(__file__).parent.parent / 'data'
    else:
        # Appelé depuis exec() dans le shell Django
        base_path = Path('migration_wordpress/data')

    json_file_django = base_path / 'articles_django.json'  # Priorité 1 : fichier converti
    json_file = base_path / 'articles.json'                # Priorité 2 : fichier manuel
    csv_file = base_path / 'articles.csv'                   # Priorité 3 : CSV

    # Détermine quel fichier utiliser
    if json_file_django.exists():
        print(f"✅ Fichier Django JSON trouvé : {json_file_django}")
        importer.import_from_json(str(json_file_django))
    elif json_file.exists():
        print(f"⚠️  Fichier articles.json trouvé (format WordPress?)")
        print(f"   Si c'est un export WordPress, lancez d'abord:")
        print(f"   python migration_wordpress/scripts/convert_wordpress_export.py\n")
        # Essaie quand même au cas où c'est le bon format
        importer.import_from_json(str(json_file))
    elif csv_file.exists():
        print(f"✅ Fichier CSV trouvé : {csv_file}")
        importer.import_from_csv(str(csv_file))
    else:
        print(f"""
❌ Aucun fichier de données trouvé !

Veuillez créer un fichier :
  - {json_file_django} (après conversion WordPress)
  - {json_file} (format manuel)
  - ou {csv_file}

Consultez la documentation du script pour le format attendu.
        """)
