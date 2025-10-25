#!/usr/bin/env python
"""
Script helper pour créer le mapping images → articles

Ce script aide à créer le dictionnaire de mapping entre les images
et les articles pour un import manuel précis.

Usage:
    python migration_wordpress/scripts/create_image_mapping.py
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amcd57_project.settings')
django.setup()

from blog.models import Article


def create_mapping_template():
    """Crée un template de mapping pour les images"""

    print("\n" + "="*70)
    print("📸 CRÉATION DU MAPPING IMAGES → ARTICLES")
    print("="*70)

    # Liste les images disponibles dans migration_wordpress/images/
    images_dir = Path('migration_wordpress/images')

    if not images_dir.exists():
        print(f"\n❌ Répertoire introuvable : {images_dir}")
        print("   Créez le répertoire et copiez vos images dedans.")
        return

    # Trouve toutes les images
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    images = []

    for img in images_dir.rglob('*'):
        if img.is_file() and img.suffix.lower() in image_extensions:
            # Chemin relatif depuis images/
            rel_path = img.relative_to(images_dir)
            images.append(str(rel_path))

    if not images:
        print(f"\n❌ Aucune image trouvée dans {images_dir}")
        print("   Copiez vos images WordPress dans ce répertoire.")
        return

    print(f"\n✅ {len(images)} image(s) trouvée(s)")
    print("\n📋 LISTE DES IMAGES :")
    print("-"*70)
    for idx, img in enumerate(sorted(images), 1):
        print(f"{idx:3}. {img}")

    # Liste les articles
    articles = Article.objects.all().order_by('titre')

    print(f"\n\n📄 LISTE DES ARTICLES ({articles.count()}) :")
    print("-"*70)
    for idx, article in enumerate(articles, 1):
        print(f"{idx:3}. {article.titre:<50} (slug: {article.slug})")

    # Crée le template de mapping
    print("\n\n" + "="*70)
    print("📝 TEMPLATE DE MAPPING À COPIER DANS import_images.py")
    print("="*70)
    print("\nCopiez le code ci-dessous dans import_images.py (ligne 342) :")
    print("\n```python")
    print("image_mapping = {")

    # Template vide pour chaque image
    for img in sorted(images)[:5]:  # Limite à 5 exemples
        print(f"    '{img}': 'slug-de-larticle',  # Exemple")

    if len(images) > 5:
        print(f"    # ... {len(images) - 5} autres images")

    print("}")
    print("```")

    # Guide d'utilisation
    print("\n\n" + "="*70)
    print("💡 GUIDE D'UTILISATION")
    print("="*70)

    print("""
1. **Pour le nom de l'image** (clé du dictionnaire) :
   - Utilisez JUSTE le nom du fichier si l'image est à la racine
     Exemple : 'image.jpg'

   - OU utilisez le chemin relatif si dans un sous-répertoire
     Exemple : '2020/01/image.jpg'

   - Le script cherchera automatiquement dans tous les sous-répertoires

2. **Pour le slug de l'article** (valeur du dictionnaire) :
   - Utilisez exactement le slug Django de l'article (voir liste ci-dessus)
   - Le slug est généré automatiquement depuis le titre

3. **Exemple complet** :

   image_mapping = {
       'reprise.jpg': 'cest-la-reprise',
       '2020/05/deconfinement.png': 'de-confinement',
       'frequences.jpg': 'la-page-des-frequences',
   }

4. **Une fois le mapping créé** :
   - Ouvrez migration_wordpress/scripts/import_images.py
   - Remplacez le dictionnaire vide (ligne 342) par votre mapping
   - Lancez : python manage.py shell < migration_wordpress/scripts/import_images.py

5. **Vérifier** :
   - Lancez : python migration_wordpress/scripts/verify_images.py
    """)

    print("="*70)


if __name__ == '__main__':
    create_mapping_template()
