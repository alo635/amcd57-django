# Migration WordPress → Django AMCD57

Ce dossier contient les outils et données pour migrer le contenu du site WordPress vers Django.

## 📁 Structure

```
migration_wordpress/
├── README.md                      # Ce fichier
├── scripts/
│   ├── import_articles.py         # Script d'import des articles
│   └── import_images.py           # Script d'import des images (à venir)
├── data/
│   ├── articles.json              # Données des articles (à créer)
│   ├── articles.json.example      # Template JSON
│   └── articles.csv.example       # Template CSV
└── images/                        # Images WordPress (à copier ici)
    ├── article-1.jpg
    ├── article-2.jpg
    └── ...
```

## 🚀 Méthode 1 : Export depuis WordPress

### 1. Exporter depuis WordPress

Dans l'admin WordPress :
1. Aller dans **Outils → Exporter**
2. Sélectionner **Articles**
3. Télécharger le fichier XML
4. Utiliser un convertisseur XML → JSON en ligne ou un script Python

### 2. Télécharger les images

Via FTP ou le panneau d'hébergement :
1. Aller dans `wp-content/uploads/`
2. Télécharger toutes les images
3. Les copier dans `migration_wordpress/images/`

## 🚀 Méthode 2 : Saisie manuelle (recommandée pour 15 articles)

### 1. Créer le fichier de données

Copier le template :
```bash
cd migration_wordpress/data
cp articles.json.example articles.json
```

### 2. Remplir articles.json

Éditer `articles.json` et ajouter vos 15 articles :

```json
{
  "articles": [
    {
      "titre": "Titre de l'article",
      "contenu": "<p>Contenu HTML complet...</p>",
      "extrait": "Résumé court (150 chars max)",
      "categorie": "Club",
      "tags": ["tag1", "tag2"],
      "date_publication": "2024-10-01 10:00:00",
      "auteur_email": "admin@amcd57.fr",
      "statut": "publie",
      "image": "nom-image.jpg",
      "meta_description": "Description SEO (160 chars max)"
    }
  ]
}
```

**Catégories disponibles** : Club, Technique, Convention, Divers

**Statuts disponibles** : `publie`, `brouillon`

### 3. Copier les images

Placer toutes les images dans :
```
migration_wordpress/images/
```

**Organisation des images** :

Le script supporte deux structures :

1. **À plat** (toutes les images à la racine) :
```
migration_wordpress/images/
├── image1.jpg
├── image2.png
└── image3.jpg
```

2. **Avec sous-répertoires** (comme WordPress : année/mois) :
```
migration_wordpress/images/
├── 2020/
│   ├── 01/
│   │   ├── image1.jpg
│   │   └── image2.png
│   └── 05/
│       └── image3.jpg
└── 2022/
    └── 09/
        └── image4.jpg
```

Le script cherche **récursivement** dans tous les sous-répertoires par défaut.

### 4. Exécuter l'import

Depuis la racine du projet Django :

```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# Lancer le script d'import
python manage.py shell
```

Dans le shell Django :
```python
exec(open('migration_wordpress/scripts/import_articles.py').read())
```

Ou en une ligne :
```bash
python manage.py shell < migration_wordpress/scripts/import_articles.py
```

## 📊 Format CSV (alternative)

Si tu préfères CSV, renommer `articles.csv.example` en `articles.csv` :

```csv
titre,contenu,extrait,categorie,tags,date_publication,auteur_email,statut,image,meta_description
"Mon article","<p>Contenu...</p>","Résumé","Club","tag1, tag2","2024-10-01 10:00:00","admin@amcd57.fr","publie","image.jpg","Description SEO"
```

**Important** : Bien entourer les champs contenant du HTML ou des virgules avec des guillemets `"`.

## 🔧 Fonctionnalités du script

### Gestion intelligente
- ✅ Crée automatiquement les catégories si inexistantes
- ✅ Crée automatiquement les tags si inexistants
- ✅ Crée automatiquement l'auteur si inexistant
- ✅ Génère les slugs automatiquement
- ✅ Détecte et met à jour les articles existants (basé sur le slug)
- ✅ Support JSON et CSV
- ✅ Statistiques détaillées d'import

### Champs optionnels
- `extrait` : Auto-généré depuis le contenu si absent
- `meta_description` : Auto-généré si absent
- `date_publication` : Utilise la date actuelle si absente
- `auteur_email` : Utilise admin@amcd57.fr par défaut
- `image` : Optionnel

## 📝 Exemple complet de migration

### Étape 1 : Préparer les données

Créer `data/articles.json` avec vos 15 articles WordPress.

### Étape 2 : Copier les images

```bash
# Option 1 : Copier à plat (toutes les images à la racine)
cp ~/Downloads/wordpress-images/* migration_wordpress/images/

# Option 2 : Copier avec la structure WordPress (année/mois)
cp -r ~/Downloads/wordpress-images/* migration_wordpress/images/
# Exemple : migration_wordpress/images/2020/01/image.jpg
```

**Le script cherche automatiquement dans tous les sous-répertoires.**

### Étape 3 : Exécuter l'import

```bash
source venv/bin/activate
python manage.py shell < migration_wordpress/scripts/import_articles.py
```

### Étape 4 : Vérifier

```bash
python manage.py shell
```

```python
from blog.models import Article
print(f"Total articles : {Article.objects.count()}")
print(f"Articles publiés : {Article.objects.filter(statut='publie').count()}")
```

### Étape 5 : Vérifier dans l'admin

Aller sur http://127.0.0.1:8000/admin/blog/article/

## 🐛 Dépannage

### Erreur "User matching query does not exist"
Créer d'abord un superuser :
```bash
python manage.py createsuperuser
```

### Erreur de format de date
Utiliser le format : `YYYY-MM-DD HH:MM:SS` (ex: `2024-10-01 14:30:00`)

### Caractères spéciaux mal affichés
S'assurer que le fichier JSON/CSV est encodé en **UTF-8**.

### Article pas visible sur le site
Vérifier que :
- `statut` = `"publie"` (pas `"brouillon"`)
- `date_publication` est dans le passé

## 📦 Script de migration des images

Le script `import_images.py` permet de :
- Copier les images depuis `migration_wordpress/images/` vers `media/blog/articles/`
- Chercher **récursivement** dans tous les sous-répertoires
- Associer automatiquement les images aux articles
- Redimensionner/optimiser les images automatiquement

### Options du script

```python
# Dans migration_wordpress/scripts/import_images.py

# Option 1 : Import automatique avec recherche récursive (par défaut)
importer.import_all_images(optimize=True, recursive=True)

# Option 2 : Import sans recherche dans les sous-répertoires
importer.import_all_images(optimize=True, recursive=False)

# Option 3 : Import avec mapping manuel (recommandé pour précision)
image_mapping = {
    'image1.jpg': 'slug-article-1',
    'image2.png': 'slug-article-2',
}
importer.copy_specific_images(image_mapping, optimize=True)
```

### Paramètres

- `optimize` : Active l'optimisation des images (redimensionnement 1200px, compression JPEG 85%)
- `recursive` : Cherche dans tous les sous-répertoires (par défaut : True)

## ✅ Checklist de migration

- [ ] Exporter les 15 articles depuis WordPress
- [ ] Créer le fichier `data/articles.json`
- [ ] Copier les 62 images dans `images/`
- [ ] Vérifier le format des données
- [ ] Exécuter le script d'import
- [ ] Vérifier dans l'admin Django
- [ ] Vérifier l'affichage frontend
- [ ] Copier les images vers `media/`
- [ ] Tester les articles sur le site
- [ ] Supprimer l'ancien WordPress (après vérification complète)

## 💡 Conseils

1. **Testez d'abord avec 1-2 articles** pour valider le processus
2. **Faites une sauvegarde de la BDD** avant l'import complet
3. **Gardez une copie des données WordPress** en backup
4. **Vérifiez le rendu HTML** des articles après import
5. **Ajustez les catégories** si nécessaire dans l'admin Django

---

**Besoin d'aide ?** Consulter le fichier `scripts/import_articles.py` pour plus de détails.
