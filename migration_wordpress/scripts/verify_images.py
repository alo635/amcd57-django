#!/usr/bin/env python
"""
Script de vérification des images importées

Ce script vérifie que les images ont été correctement importées et associées aux articles.

Usage:
    python migration_wordpress/scripts/verify_images.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amcd57_project.settings')
django.setup()

from django.conf import settings
from blog.models import Article


def verify_images():
    """Vérifie l'import des images"""

    print("\n" + "="*70)
    print("📸 VÉRIFICATION DES IMAGES IMPORTÉES")
    print("="*70)

    # Statistiques
    stats = {
        'total_articles': 0,
        'articles_avec_image': 0,
        'articles_sans_image': 0,
        'images_existantes': 0,
        'images_manquantes': 0,
        'images_vides': 0
    }

    articles = Article.objects.all().order_by('-date_publication')
    stats['total_articles'] = articles.count()

    print(f"\n📊 Total articles : {stats['total_articles']}")
    print("\n" + "-"*70)
    print(f"{'Article':<40} {'Image':<20} {'Statut'}")
    print("-"*70)

    articles_avec_probleme = []

    for article in articles:
        titre_court = article.titre[:37] + "..." if len(article.titre) > 40 else article.titre

        if article.image:
            stats['articles_avec_image'] += 1
            image_nom = Path(article.image.name).name if hasattr(article.image, 'name') else str(article.image)[:17]

            # Vérifie si le fichier existe
            image_path = Path(settings.MEDIA_ROOT) / str(article.image)

            if image_path.exists():
                # Vérifie que le fichier n'est pas vide
                if image_path.stat().st_size > 0:
                    stats['images_existantes'] += 1
                    statut = "✅ OK"
                else:
                    stats['images_vides'] += 1
                    statut = "⚠️  VIDE"
                    articles_avec_probleme.append({
                        'titre': article.titre,
                        'image': image_nom,
                        'probleme': 'Fichier vide (0 octets)'
                    })
            else:
                stats['images_manquantes'] += 1
                statut = "❌ MANQUANT"
                articles_avec_probleme.append({
                    'titre': article.titre,
                    'image': image_nom,
                    'probleme': f'Fichier introuvable : {image_path}'
                })
        else:
            stats['articles_sans_image'] += 1
            image_nom = "-"
            statut = "⚪ Pas d'image"

        print(f"{titre_court:<40} {image_nom:<20} {statut}")

    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ")
    print("="*70)
    print(f"Total articles              : {stats['total_articles']}")
    print(f"Articles avec image         : {stats['articles_avec_image']}")
    print(f"Articles sans image         : {stats['articles_sans_image']}")
    print(f"Images existantes et OK     : {stats['images_existantes']} ✅")
    print(f"Images manquantes           : {stats['images_manquantes']} ❌")
    print(f"Images vides (0 octets)     : {stats['images_vides']} ⚠️")

    # Pourcentages
    if stats['articles_avec_image'] > 0:
        taux_succes = (stats['images_existantes'] / stats['articles_avec_image']) * 100
        print(f"\n📈 Taux de succès           : {taux_succes:.1f}%")

    # Détails des problèmes
    if articles_avec_probleme:
        print("\n" + "="*70)
        print("⚠️  ARTICLES AVEC PROBLÈMES D'IMAGES")
        print("="*70)
        for idx, article in enumerate(articles_avec_probleme, 1):
            print(f"\n{idx}. {article['titre']}")
            print(f"   Image   : {article['image']}")
            print(f"   Problème: {article['probleme']}")

    # Vérification du répertoire media
    print("\n" + "="*70)
    print("📁 VÉRIFICATION RÉPERTOIRE MEDIA")
    print("="*70)

    media_blog_path = Path(settings.MEDIA_ROOT) / 'blog' / 'articles'

    if media_blog_path.exists():
        # Compte les images dans media/blog/articles/
        images_in_media = list(media_blog_path.rglob('*'))
        image_files = [f for f in images_in_media if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']]

        print(f"Chemin media                : {media_blog_path}")
        print(f"Total fichiers images       : {len(image_files)}")

        # Grouper par année/mois
        annees = {}
        for img in image_files:
            parts = img.parts
            if len(parts) >= 2:
                year = parts[-3] if len(parts) >= 3 else 'racine'
                month = parts[-2] if len(parts) >= 2 else 'racine'
                key = f"{year}/{month}"
                annees[key] = annees.get(key, 0) + 1

        if annees:
            print(f"\nDistribution par dossier :")
            for folder, count in sorted(annees.items()):
                print(f"  - {folder} : {count} image(s)")
    else:
        print(f"⚠️  Répertoire media introuvable : {media_blog_path}")
        print(f"   Exécutez le script import_images.py pour créer la structure")

    # Images orphelines
    if media_blog_path.exists() and image_files:
        print("\n" + "="*70)
        print("🔍 RECHERCHE IMAGES ORPHELINES")
        print("="*70)

        # Images dans media
        images_media_set = {f.name for f in image_files}

        # Images dans articles
        images_articles = [Path(a.image.name).name for a in articles if a.image]
        images_articles_set = set(images_articles)

        # Orphelines = dans media mais pas dans articles
        orphelines = images_media_set - images_articles_set

        if orphelines:
            print(f"⚠️  {len(orphelines)} image(s) orpheline(s) trouvée(s) :")
            for img in sorted(orphelines):
                print(f"   - {img}")
            print("\nCes images sont dans media/ mais pas associées à des articles.")
        else:
            print("✅ Aucune image orpheline trouvée")

    # Recommandations
    print("\n" + "="*70)
    print("💡 RECOMMANDATIONS")
    print("="*70)

    if stats['images_manquantes'] > 0:
        print(f"❌ {stats['images_manquantes']} image(s) manquante(s)")
        print("   → Relancer le script import_images.py")
        print("   → Vérifier que les images sont dans migration_wordpress/images/")

    if stats['images_vides'] > 0:
        print(f"⚠️  {stats['images_vides']} image(s) vide(s)")
        print("   → Vérifier les fichiers sources")
        print("   → Copier à nouveau les images depuis WordPress")

    if stats['articles_sans_image'] > 0:
        print(f"ℹ️  {stats['articles_sans_image']} article(s) sans image")
        print("   → Normal si certains articles n'ont pas d'image à la une")

    if stats['images_existantes'] == stats['articles_avec_image'] and stats['articles_avec_image'] > 0:
        print("✅ Toutes les images sont correctement importées !")

    print("\n" + "="*70)

    # Code de sortie
    if stats['images_manquantes'] > 0 or stats['images_vides'] > 0:
        return 1  # Erreur
    return 0  # Succès


if __name__ == '__main__':
    exit_code = verify_images()
    sys.exit(exit_code)
