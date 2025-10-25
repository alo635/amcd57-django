#!/usr/bin/env python
"""
Script pour corriger les URLs d'images dans le contenu des articles

Ce script :
1. Trouve toutes les images référencées dans le contenu HTML des articles
2. Met à jour les URLs pour pointer vers /media/blog/articles/
3. Copie les images WordPress vers media/

Usage:
    python migration_wordpress/scripts/fix_content_images.py
"""

import os
import sys
import re
import django
from pathlib import Path
import shutil

# Setup Django
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amcd57_project.settings')
django.setup()

from django.conf import settings
from blog.models import Article


def find_images_in_content(html_content):
    """
    Trouve toutes les images dans le contenu HTML

    Patterns supportés :
    - <img src="..." />
    - <img src='...' />
    - URLs WordPress : http://localhost:8888/amcd57/wp-content/uploads/2020/11/image.jpg
    """
    # Pattern pour trouver les balises img
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'

    images = []
    matches = re.finditer(img_pattern, html_content, re.IGNORECASE)

    for match in matches:
        full_tag = match.group(0)
        src = match.group(1)
        images.append({
            'full_tag': full_tag,
            'src': src
        })

    return images


def extract_wordpress_path(url):
    """
    Extrait le chemin de l'image depuis une URL WordPress

    Exemples :
    - http://localhost:8888/amcd57/wp-content/uploads/2020/11/image.jpg
      → 2020/11/image.jpg
    - /wp-content/uploads/2020/11/image.jpg
      → 2020/11/image.jpg
    """
    # Pattern pour wp-content/uploads/...
    wp_pattern = r'wp-content/uploads/(.+?)(?:\?|$|"|\s)'
    match = re.search(wp_pattern, url)

    if match:
        return match.group(1)

    # Si c'est déjà un chemin relatif comme 2020/11/image.jpg
    if '/' in url and not url.startswith('http'):
        return url

    return None


def fix_article_images():
    """Corrige les images dans tous les articles"""

    print("\n" + "="*70)
    print("🔧 CORRECTION DES IMAGES DANS LE CONTENU DES ARTICLES")
    print("="*70)

    articles = Article.objects.all()

    stats = {
        'articles_checked': 0,
        'articles_with_images': 0,
        'images_found': 0,
        'images_copied': 0,
        'images_skipped': 0,
        'articles_updated': 0
    }

    wordpress_images_dir = Path('migration_wordpress/images')
    media_dir = Path(settings.MEDIA_ROOT) / 'blog' / 'articles'

    for article in articles:
        stats['articles_checked'] += 1

        # Trouve les images dans le contenu
        images = find_images_in_content(article.contenu)

        if not images:
            continue

        stats['articles_with_images'] += 1
        stats['images_found'] += len(images)

        print(f"\n📄 {article.titre}")
        print(f"   {len(images)} image(s) trouvée(s) dans le contenu")

        new_content = article.contenu
        content_modified = False

        for img_info in images:
            src = img_info['src']

            # Extrait le chemin WordPress
            wp_path = extract_wordpress_path(src)

            if not wp_path:
                print(f"   ⏭️  Ignoré : {src[:50]}... (pas une image WordPress)")
                stats['images_skipped'] += 1
                continue

            print(f"   📸 {wp_path}")

            # Cherche l'image source
            source_path = wordpress_images_dir / wp_path

            if not source_path.exists():
                print(f"      ❌ Source introuvable : {source_path}")
                stats['images_skipped'] += 1
                continue

            # Destination dans media/blog/articles/
            # Garde la structure année/mois de WordPress
            dest_path = media_dir / wp_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copie l'image si pas déjà présente
            if not dest_path.exists():
                shutil.copy2(source_path, dest_path)
                print(f"      ✅ Copié vers : media/blog/articles/{wp_path}")
                stats['images_copied'] += 1
            else:
                print(f"      ℹ️  Déjà présent : media/blog/articles/{wp_path}")

            # Met à jour l'URL dans le contenu
            new_url = f"/media/blog/articles/{wp_path}"
            new_content = new_content.replace(src, new_url)
            content_modified = True

        # Sauvegarde l'article si modifié
        if content_modified:
            article.contenu = new_content
            article.save(update_fields=['contenu'])
            stats['articles_updated'] += 1
            print(f"   ✅ Article mis à jour")

    # Affiche les statistiques
    print("\n" + "="*70)
    print("📊 STATISTIQUES")
    print("="*70)
    print(f"Articles vérifiés           : {stats['articles_checked']}")
    print(f"Articles avec images        : {stats['articles_with_images']}")
    print(f"Images trouvées             : {stats['images_found']}")
    print(f"Images copiées              : {stats['images_copied']}")
    print(f"Images ignorées             : {stats['images_skipped']}")
    print(f"Articles mis à jour         : {stats['articles_updated']}")
    print("="*70 + "\n")

    if stats['images_copied'] > 0:
        print("✅ Les images ont été copiées et les URLs mises à jour !")
        print("\n📌 Vérifiez vos articles sur : http://127.0.0.1:8000/blog/")
    else:
        print("ℹ️  Aucune image à copier (toutes déjà présentes ou aucune trouvée)")


if __name__ == '__main__':
    fix_article_images()
