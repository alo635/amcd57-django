#!/usr/bin/env python
"""
Script de migration des images WordPress vers Django AMCD57

Ce script :
1. Copie les images depuis migration_wordpress/images/ vers media/blog/articles/
2. Associe les images aux articles correspondants
3. Optionnel : Redimensionne/optimise les images

Usage:
    python manage.py shell < migration_wordpress/scripts/import_images.py

    Ou dans le shell Django :
    exec(open('migration_wordpress/scripts/import_images.py').read())
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
from django.conf import settings
from django.core.files import File
from blog.models import Article


class ImageImporter:
    """Classe pour gérer l'import des images WordPress"""

    def __init__(self, source_dir='migration_wordpress/images'):
        """
        Initialise l'importeur d'images

        Args:
            source_dir: Répertoire source contenant les images WordPress
        """
        self.source_dir = Path(source_dir)
        self.media_root = Path(settings.MEDIA_ROOT)
        self.stats = {
            'images_copied': 0,
            'images_skipped': 0,
            'articles_updated': 0,
            'errors': []
        }

    def get_destination_path(self, filename, date=None):
        """
        Génère le chemin de destination pour une image

        Les images sont organisées par année/mois comme dans le modèle Article :
        media/blog/articles/2024/10/filename.jpg

        Args:
            filename: Nom du fichier image
            date: Date de publication (optionnel, utilise la date actuelle si absent)

        Returns:
            Path: Chemin complet de destination
        """
        date = date or datetime.now()
        year = date.strftime('%Y')
        month = date.strftime('%m')

        dest_dir = self.media_root / 'blog' / 'articles' / year / month
        dest_dir.mkdir(parents=True, exist_ok=True)

        return dest_dir / filename

    def optimize_image(self, image_path, max_width=1200, quality=85):
        """
        Optimise une image (redimensionnement et compression)

        Args:
            image_path: Chemin de l'image
            max_width: Largeur maximale en pixels
            quality: Qualité JPEG (0-100)
        """
        try:
            with Image.open(image_path) as img:
                # Redimensionne si trop large
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # Convertit en RGB si nécessaire (pour JPEG)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                # Sauvegarde avec compression
                img.save(image_path, 'JPEG', quality=quality, optimize=True)

                print(f"  ✅ Image optimisée : {image_path.name}")
                return True

        except Exception as e:
            print(f"  ⚠️  Erreur d'optimisation pour {image_path.name}: {e}")
            return False

    def copy_image(self, source_path, dest_path, optimize=True):
        """
        Copie une image depuis la source vers la destination

        Args:
            source_path: Chemin source
            dest_path: Chemin destination
            optimize: Si True, optimise l'image après copie

        Returns:
            bool: True si succès, False sinon
        """
        try:
            # Copie le fichier
            shutil.copy2(source_path, dest_path)

            # Optimise si demandé
            if optimize and dest_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                self.optimize_image(dest_path)

            return True

        except Exception as e:
            error_msg = f"Erreur lors de la copie de {source_path.name}: {e}"
            print(f"  ❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            return False

    def associate_image_to_article(self, article, image_filename):
        """
        Associe une image à un article

        Args:
            article: Instance Article
            image_filename: Nom du fichier image
        """
        # Construit le chemin relatif depuis MEDIA_ROOT
        date_pub = article.date_publication or datetime.now()
        year = date_pub.strftime('%Y')
        month = date_pub.strftime('%m')

        relative_path = f"blog/articles/{year}/{month}/{image_filename}"

        # Met à jour l'article
        article.image = relative_path
        article.save(update_fields=['image'])

        print(f"  ✅ Image associée à l'article : {article.titre}")
        self.stats['articles_updated'] += 1

    def import_all_images(self, optimize=True, recursive=True):
        """
        Importe toutes les images depuis le répertoire source

        Args:
            optimize: Si True, optimise les images pendant l'import
            recursive: Si True, cherche aussi dans les sous-répertoires
        """
        print(f"\n📥 Import des images depuis : {self.source_dir}")
        if recursive:
            print(f"   Mode récursif : recherche dans les sous-répertoires activée")

        if not self.source_dir.exists():
            print(f"❌ Répertoire source introuvable : {self.source_dir}")
            return False

        # Liste toutes les images
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

        if recursive:
            # Recherche récursive dans tous les sous-répertoires
            images = [
                f for f in self.source_dir.rglob('*')
                if f.is_file() and f.suffix.lower() in image_extensions
            ]
        else:
            # Recherche uniquement dans le répertoire racine
            images = [
                f for f in self.source_dir.iterdir()
                if f.is_file() and f.suffix.lower() in image_extensions
            ]

        if not images:
            print(f"❌ Aucune image trouvée dans {self.source_dir}")
            return False

        print(f"📊 {len(images)} image(s) trouvée(s)\n")

        for idx, image_path in enumerate(images, 1):
            print(f"[{idx}/{len(images)}] {image_path.name}")

            # Cherche un article correspondant
            article = self.find_article_for_image(image_path.name)

            if article:
                # Copie vers le bon répertoire (organisé par date de l'article)
                dest_path = self.get_destination_path(
                    image_path.name,
                    article.date_publication
                )

                if self.copy_image(image_path, dest_path, optimize):
                    self.associate_image_to_article(article, image_path.name)
                    self.stats['images_copied'] += 1
                else:
                    self.stats['images_skipped'] += 1
            else:
                # Pas d'article trouvé, copie quand même dans le dossier actuel
                dest_path = self.get_destination_path(image_path.name)

                if self.copy_image(image_path, dest_path, optimize):
                    print(f"  ⚠️  Image copiée mais aucun article associé")
                    self.stats['images_copied'] += 1
                else:
                    self.stats['images_skipped'] += 1

        self.print_stats()
        return True

    def find_article_for_image(self, image_filename):
        """
        Trouve l'article correspondant à une image

        Stratégies :
        1. Cherche un article avec ce nom d'image dans le champ image
        2. Cherche par similarité de nom (slug vs nom fichier)

        Args:
            image_filename: Nom du fichier image

        Returns:
            Article ou None
        """
        # Stratégie 1 : Recherche exacte dans le champ image
        article = Article.objects.filter(image__icontains=image_filename).first()
        if article:
            return article

        # Stratégie 2 : Par slug similaire
        # Extrait le nom sans extension
        name_without_ext = Path(image_filename).stem

        # Cherche un article avec un slug similaire
        article = Article.objects.filter(slug__icontains=name_without_ext).first()
        if article:
            print(f"  ℹ️  Article trouvé par similarité de slug : {article.titre}")
            return article

        print(f"  ⚠️  Aucun article trouvé pour l'image {image_filename}")
        return None

    def copy_specific_images(self, image_mapping, optimize=True):
        """
        Copie des images spécifiques avec mapping article

        Args:
            image_mapping: Dict {image_filename: article_slug}
            optimize: Si True, optimise les images

        Example:
            {
                'article-1.jpg': 'mon-premier-article',
                'article-2.jpg': 'deuxieme-article'
            }
        """
        print(f"\n📥 Import d'images avec mapping personnalisé")
        print(f"📊 {len(image_mapping)} image(s) à importer\n")

        for idx, (image_filename, article_slug) in enumerate(image_mapping.items(), 1):
            print(f"[{idx}/{len(image_mapping)}] {image_filename} → {article_slug}")

            # Cherche l'article
            try:
                article = Article.objects.get(slug=article_slug)
            except Article.DoesNotExist:
                error_msg = f"Article introuvable : {article_slug}"
                print(f"  ❌ {error_msg}")
                self.stats['errors'].append(error_msg)
                self.stats['images_skipped'] += 1
                continue

            # Cherche l'image source
            source_path = self.source_dir / image_filename

            if not source_path.exists():
                error_msg = f"Image introuvable : {image_filename}"
                print(f"  ❌ {error_msg}")
                self.stats['errors'].append(error_msg)
                self.stats['images_skipped'] += 1
                continue

            # Extrait juste le nom du fichier (sans le chemin)
            just_filename = Path(image_filename).name

            # Copie et associe
            dest_path = self.get_destination_path(
                just_filename,
                article.date_publication
            )

            if self.copy_image(source_path, dest_path, optimize):
                self.associate_image_to_article(article, just_filename)
                self.stats['images_copied'] += 1
            else:
                self.stats['images_skipped'] += 1

        self.print_stats()

    def print_stats(self):
        """Affiche les statistiques d'import"""
        print("\n" + "="*60)
        print("📊 STATISTIQUES D'IMPORT DES IMAGES")
        print("="*60)
        print(f"Images copiées       : {self.stats['images_copied']}")
        print(f"Images ignorées      : {self.stats['images_skipped']}")
        print(f"Articles mis à jour  : {self.stats['articles_updated']}")
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
    ║  SCRIPT D'IMPORT DES IMAGES WORDPRESS → DJANGO AMCD57        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    # Initialise l'importeur
    importer = ImageImporter(source_dir='migration_wordpress/images')

    # Option 1 : Import automatique (cherche les correspondances)
    # importer.import_all_images(optimize=True, recursive=True)

    # Option 2 : Import avec mapping manuel (recommandé)
    # Exemple de mapping personnalisé
    image_mapping = {
        #inter-ex-2022-vittersbourg-57
        '2022/09/P1030409.jpg': 'inter-ex-2022-vittersbourg-57',
        # antennes-de-rechange-24ghz-bis
        '2020/11/Vue_plandemasse_ant.jpg': 'antennes-de-rechange-24ghz-bis',
        # antennes-de-rechange-24ghz
        '2020/11/PC.jpg': 'antennes-de-rechange-24ghz',
        # cle-de-contact-pour-aeronef-electrique
        '2020/11/cl_contact.jpg': 'cle-de-contact-pour-aeronef-electrique',
        # convention-avec-le-cen
        '2020/11/logo_conservatoire_2013.png': 'convention-avec-le-cen',
        # convention-avec-la-dgac
        '2020/11/logo_DGAC.jpg': 'convention-avec-la-dgac',
        # convention-avec-la-cnil
        '2020/11/logo_cnil.jpg': 'convention-avec-la-cnil',
        # ou-volons-nous
        '2020/01/pente_sud_medium.jpg': 'ou-volons-nous',
        # la-page-des-frequences
        '2020/11/panneaux.jpg': 'la-page-des-frequences',
    }

    if image_mapping:
        print("✅ Utilisation du mapping personnalisé")
        importer.copy_specific_images(image_mapping, optimize=True)
    else:
        print("✅ Import automatique des images")
        print("   Options :")
        print("   - recursive=True : cherche dans tous les sous-répertoires")
        print("   - recursive=False : cherche uniquement à la racine")
        importer.import_all_images(optimize=True, recursive=True)

    print("""
    ✅ Import terminé !

    Vérifier les images dans :
      - Admin : http://127.0.0.1:8000/admin/blog/article/
      - Frontend : http://127.0.0.1:8000/blog/

    Les images sont stockées dans :
      - media/blog/articles/YYYY/MM/
    """)
