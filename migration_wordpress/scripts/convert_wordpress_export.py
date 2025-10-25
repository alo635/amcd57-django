#!/usr/bin/env python
"""
Script de conversion d'export WordPress (XML→JSON) vers format Django

Ce script convertit un export WordPress au format JSON (converti depuis XML)
vers le format simple attendu par import_articles.py

Usage:
    python migration_wordpress/scripts/convert_wordpress_export.py
"""

import json
import re
from pathlib import Path
from datetime import datetime


def clean_html_content(html):
    """Nettoie le contenu HTML WordPress (enlève les balises Gutenberg)"""
    if not html:
        return ""

    # Enlève les commentaires Gutenberg
    html = re.sub(r'<!-- wp:.*?-->', '', html)
    html = re.sub(r'<!-- /wp:.*?-->', '', html)

    # Nettoie les espaces multiples
    html = re.sub(r'\n\s*\n', '\n', html)

    return html.strip()


def extract_excerpt(content, max_length=150):
    """Extrait un résumé depuis le contenu HTML"""
    # Enlève les balises HTML
    text = re.sub(r'<[^>]+>', '', content)
    # Enlève les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    # Tronque
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + '...'
    return text.strip()


def convert_wordpress_export(input_file, output_file):
    """
    Convertit un export WordPress JSON vers le format Django

    Args:
        input_file: Chemin du fichier WordPress JSON
        output_file: Chemin du fichier de sortie
    """
    print(f"\n🔄 CONVERSION EXPORT WORDPRESS")
    print("="*60)
    print(f"Entrée  : {input_file}")
    print(f"Sortie  : {output_file}\n")

    # Charge le fichier WordPress
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            wp_data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur de lecture : {e}")
        return False

    # Extrait les items (articles)
    try:
        items = wp_data['rss']['channel']['item']
        if not isinstance(items, list):
            items = [items]
    except KeyError:
        print("❌ Structure WordPress invalide (pas de rss/channel/item)")
        return False

    print(f"📊 {len(items)} items trouvés dans l'export WordPress\n")

    # Convertit chaque item
    articles = []
    stats = {
        'converted': 0,
        'skipped': 0,
        'posts': 0,
        'pages': 0,
        'other': 0
    }

    for idx, item in enumerate(items, 1):
        # Extrait le type de post
        post_type = item.get('post_type', {})
        if isinstance(post_type, dict):
            post_type = post_type.get('__cdata', 'post')

        # Filtre : garde seulement les posts (articles)
        if post_type != 'post':
            print(f"[{idx}/{len(items)}] ⏭️  Ignoré ({post_type}): {item.get('title', 'Sans titre')}")
            stats['skipped'] += 1
            if post_type == 'page':
                stats['pages'] += 1
            else:
                stats['other'] += 1
            continue

        stats['posts'] += 1

        # Vérifie le statut (seulement les publiés)
        status = item.get('status', {})
        if isinstance(status, dict):
            status = status.get('__cdata', 'publish')

        if status != 'publish':
            print(f"[{idx}/{len(items)}] ⏭️  Ignoré (brouillon): {item.get('title', 'Sans titre')}")
            stats['skipped'] += 1
            continue

        print(f"[{idx}/{len(items)}] ✅ Conversion: {item.get('title', 'Sans titre')}")

        # Extrait le contenu
        content = ""
        encoded = item.get('encoded', [])
        if isinstance(encoded, list):
            for enc in encoded:
                if isinstance(enc, dict) and enc.get('__prefix') == 'content':
                    content = enc.get('__cdata', '')
                    break
        elif isinstance(encoded, dict):
            content = encoded.get('__cdata', '')

        content = clean_html_content(content)

        # Extrait l'extrait
        excerpt = ""
        if isinstance(encoded, list):
            for enc in encoded:
                if isinstance(enc, dict) and enc.get('__prefix') == 'excerpt':
                    excerpt = enc.get('__cdata', '')
                    break

        # Si pas d'extrait, génère-le depuis le contenu
        if not excerpt:
            excerpt = extract_excerpt(content)

        # Extrait la catégorie
        category = item.get('category', {})
        if isinstance(category, list):
            # Prend la première catégorie non vide
            category = next((c for c in category if c), {})

        category_name = "Divers"  # Par défaut
        if isinstance(category, dict):
            category_name = category.get('__cdata', 'Divers')
        elif isinstance(category, str):
            category_name = category

        # Extrait les tags (dans WordPress, peuvent être dans category avec domain="post_tag")
        tags = []
        categories = item.get('category', [])
        if not isinstance(categories, list):
            categories = [categories] if categories else []

        for cat in categories:
            if isinstance(cat, dict):
                domain = cat.get('_domain', '')
                if domain == 'post_tag':
                    tag_name = cat.get('__cdata', '')
                    if tag_name:
                        tags.append(tag_name)

        # Extrait la date de publication
        post_date = item.get('post_date', {})
        if isinstance(post_date, dict):
            post_date = post_date.get('__cdata', '')

        # Format : 2020-05-30 19:17:55
        if post_date:
            try:
                # Convertit au format attendu
                dt = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
                post_date_formatted = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                post_date_formatted = post_date
        else:
            post_date_formatted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Extrait l'auteur
        creator = item.get('creator', {})
        if isinstance(creator, dict):
            creator = creator.get('__cdata', 'denis')

        author_email = f"{creator}@amcd57.fr"  # Génère un email

        # Construit l'article au format Django
        article = {
            "titre": item.get('title', 'Sans titre'),
            "contenu": content,
            "extrait": excerpt,
            "categorie": category_name,
            "tags": tags,
            "date_publication": post_date_formatted,
            "auteur_email": author_email,
            "auteur_username": creator,
            "statut": "publie",
            "image": "",  # À compléter manuellement si nécessaire
            "meta_description": excerpt[:160] if len(excerpt) > 160 else excerpt
        }

        articles.append(article)
        stats['converted'] += 1

    # Sauvegarde au format Django
    django_data = {
        "articles": articles
    }

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(django_data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Conversion réussie !")
    except Exception as e:
        print(f"\n❌ Erreur d'écriture : {e}")
        return False

    # Affiche les stats
    print("\n" + "="*60)
    print("📊 STATISTIQUES DE CONVERSION")
    print("="*60)
    print(f"Articles convertis   : {stats['converted']}")
    print(f"Articles ignorés     : {stats['skipped']}")
    print(f"  - Pages            : {stats['pages']}")
    print(f"  - Autres types     : {stats['other']}")
    print(f"  - Brouillons       : {stats['skipped'] - stats['pages'] - stats['other']}")
    print(f"\nTotal posts WP       : {stats['posts']}")
    print(f"Total items WP       : {len(items)}")
    print("="*60 + "\n")

    print(f"📄 Fichier créé : {output_file}")
    print(f"📦 {len(articles)} articles prêts pour l'import Django\n")

    return True


if __name__ == '__main__':
    # Chemins des fichiers
    base_dir = Path(__file__).parent.parent
    input_file = base_dir / 'data' / 'articles.json'
    output_file = base_dir / 'data' / 'articles_django.json'

    # Vérifie que le fichier d'entrée existe
    if not input_file.exists():
        print(f"❌ Fichier introuvable : {input_file}")
        print("\nAssurez-vous d'avoir placé l'export WordPress dans :")
        print(f"  {input_file}")
        exit(1)

    # Lance la conversion
    success = convert_wordpress_export(str(input_file), str(output_file))

    if success:
        print("✅ Conversion terminée !")
        print("\n📌 Prochaine étape :")
        print("   1. Vérifier articles_django.json")
        print("   2. Lancer l'import :")
        print("      python manage.py shell")
        print("      >>> exec(open('migration_wordpress/scripts/import_articles.py').read())")
    else:
        print("❌ La conversion a échoué")
        exit(1)
