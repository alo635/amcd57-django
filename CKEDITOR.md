# 📝 Guide CKEditor - AMCD57

## Vue d'ensemble

Ce guide explique l'utilisation de **CKEditor** dans l'administration Django du projet AMCD57. CKEditor est un éditeur WYSIWYG (What You See Is What You Get) qui permet de créer et éditer du contenu HTML de manière visuelle, sans avoir à écrire directement le code HTML.

**Version installée** : django-ckeditor 6.7.1
**Date d'intégration** : 29 octobre 2025
**Utilisé dans** : Articles de blog (champ `contenu`)

---

## 🎯 Fonctionnalités

### ✅ Formatage de texte
- **Gras**, *Italique*, <u>Souligné</u>, ~~Barré~~
- Styles de paragraphe (Normal, Titre 1-6, Citation)
- Couleurs de texte et surlignage
- Suppression de formatage

### ✅ Listes et indentation
- Listes numérotées (1, 2, 3...)
- Listes à puces (•)
- Indentation / Désindentation
- Citations (blockquote)

### ✅ Liens et ancres
- Insertion de liens hypertextes
- Configuration des attributs de liens (target, title, etc.)
- Ancres internes pour navigation dans le document
- Suppression de liens

### ✅ Images
- **Upload d'images directement dans l'éditeur**
- Insertion d'images depuis le serveur
- Redimensionnement visuel des images
- Alignement (gauche, centre, droite)
- Texte alternatif (alt) pour l'accessibilité
- Organisation automatique par date : `media/blog/articles/YYYY/MM/`

### ✅ Tableaux
- Création de tableaux
- Ajout/suppression de lignes et colonnes
- Fusion de cellules
- Propriétés des cellules

### ✅ Autres fonctionnalités
- Caractères spéciaux (©, ®, €, etc.)
- Ligne horizontale
- Code source HTML (mode avancé)
- Plein écran pour édition confortable
- Annuler / Refaire

---

## 🚀 Utilisation dans l'admin Django

### Accéder à l'éditeur

1. Connectez-vous à l'admin Django : `http://127.0.0.1:8000/admin/` (développement) ou `https://amcd.alodev.ovh/admin/` (production)
2. Naviguez vers **Blog → Articles**
3. Cliquez sur un article existant ou créez-en un nouveau
4. Le champ **Contenu** affiche automatiquement l'éditeur CKEditor

### Créer un article avec CKEditor

#### 1. Informations de base
- **Titre** : Titre de l'article
- **Slug** : Généré automatiquement depuis le titre (modifiable)
- **Auteur** : Sélectionnez l'auteur
- **Catégorie** : Choisissez une catégorie
- **Tags** : Ajoutez des tags (optionnel)

#### 2. Éditer le contenu

**Écriture de texte** :
- Tapez directement dans l'éditeur comme dans un traitement de texte
- Sélectionnez le texte pour appliquer du formatage (gras, italique, etc.)
- Utilisez la liste déroulante "Format" pour les titres et styles

**Insérer une image** :
1. Cliquez sur l'icône **Image** dans la barre d'outils
2. Onglet "Upload" : cliquez sur **Choose File** et sélectionnez votre image
3. Cliquez sur **Send it to the Server**
4. L'image est uploadée dans `media/blog/articles/2025/10/` (par exemple)
5. Configurez les propriétés de l'image :
   - **Alt Text** : Description de l'image (important pour l'accessibilité)
   - **Width/Height** : Dimensions en pixels
   - **Alignment** : Gauche, Centre, Droite
6. Cliquez sur **OK**

**Insérer un lien** :
1. Sélectionnez le texte à transformer en lien
2. Cliquez sur l'icône **Link**
3. **URL** : Entrez l'URL complète (ex: `https://exemple.com`)
4. **Target** : Choisissez "_blank" pour ouvrir dans un nouvel onglet
5. Cliquez sur **OK**

**Insérer un tableau** :
1. Cliquez sur l'icône **Table**
2. Configurez :
   - Nombre de lignes et colonnes
   - Largeur (% ou pixels)
   - En-têtes (première ligne/colonne)
3. Cliquez sur **OK**
4. Remplissez les cellules
5. Clic droit sur le tableau pour modifier sa structure

#### 3. Autres champs

- **Extrait** : Laissez vide pour génération automatique (premiers 150 caractères du contenu)
- **Image à la une** : Upload séparé pour l'image principale de l'article
- **Statut** :
  - **Brouillon** : Article non visible publiquement
  - **Publié** : Article visible sur le site
- **Date de publication** : Automatiquement définie lors de la publication

#### 4. Sauvegarder

- **Enregistrer et continuer** : Sauvegarde sans quitter l'éditeur
- **Enregistrer et ajouter un autre** : Sauvegarde et ouvre un nouvel article
- **Enregistrer** : Sauvegarde et retourne à la liste des articles

---

## 💡 Bonnes pratiques

### Images

✅ **À faire** :
- Optimiser les images avant l'upload (recommandé : max 1200px de largeur)
- Toujours ajouter un texte alternatif (alt) descriptif
- Utiliser des formats web (JPEG pour photos, PNG pour graphiques, WebP si possible)
- Nommer les fichiers de manière descriptive (`club-amcd57.jpg` plutôt que `IMG_1234.jpg`)

❌ **À éviter** :
- Uploader des images trop lourdes (> 2 MB)
- Utiliser des formats inadaptés (BMP, TIFF)
- Oublier le texte alternatif (mauvais pour l'accessibilité et le SEO)

### Structure du contenu

✅ **À faire** :
- Utiliser les titres hiérarchiquement (H2 → H3 → H4)
- Aérer le texte avec des paragraphes courts
- Utiliser des listes pour énumérer des éléments
- Ajouter des liens vers des sources ou articles connexes

❌ **À éviter** :
- Utiliser les titres uniquement pour la taille de police
- Faire des paragraphes de plus de 5-6 lignes
- Abuser du gras et de l'italique (1-2 mots maximum par utilisation)

### Formatage

✅ **À faire** :
- Rester cohérent dans le formatage (toujours les mêmes styles pour les mêmes types de contenu)
- Utiliser la fonction "Supprimer le formatage" si vous copiez-collez du texte depuis Word/Google Docs
- Vérifier le rendu en mode "Source" de temps en temps

❌ **À éviter** :
- Coller du contenu directement depuis Word (crée du HTML complexe inutile)
- Utiliser trop de couleurs ou de polices différentes
- Mélanger les styles (ex: gras + souligné + italique en même temps)

### Accessibilité

✅ **À faire** :
- Toujours remplir l'attribut `alt` des images
- Utiliser la structure de titres appropriée (H2, H3, etc.)
- Créer des liens avec du texte descriptif ("En savoir plus sur le club" plutôt que "Cliquez ici")
- Vérifier le contraste des couleurs de texte

### SEO (Référencement)

✅ **À faire** :
- Utiliser des mots-clés pertinents dans les titres
- Rédiger des textes de liens descriptifs
- Optimiser les noms de fichiers images
- Remplir le champ "Extrait" ou laisser la génération automatique faire

---

## 🔧 Configuration technique

### Paramètres CKEditor (settings.py)

```python
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', 'Blockquote', 'Indent', 'Outdent'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Undo', 'Redo'],
            ['Maximize'],
            ['Source'],
        ],
        'height': 500,
        'width': '100%',
        'language': 'fr',
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
        'extraAllowedContent': 'img[*]{*}(*);figure[*]{*}(*);figcaption[*]{*}(*)',
    },
}
```

### Chemins de stockage

- **Images CKEditor** : `media/blog/articles/%Y/%m/` (organisé par année et mois)
- **Images à la une** : `media/blog/articles/%Y/%m/` (même répertoire, gestion séparée)
- **Configuration** : `CKEDITOR_UPLOAD_PATH = 'blog/articles/%Y/%m/'`

### Restrictions de sécurité

- **Types de fichiers autorisés** : Images uniquement (JPEG, PNG, GIF, WebP)
- **Taille maximale** : 10 MB (limite Django : `DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760`)
- **Restriction par utilisateur** : `CKEDITOR_RESTRICT_BY_USER = True` (chaque utilisateur ne voit que ses propres uploads)

---

## 🐛 Dépannage

### L'éditeur ne s'affiche pas

**Symptôme** : Le champ Contenu affiche un simple textarea au lieu de CKEditor

**Solutions** :
1. Vérifier que CKEditor est dans `INSTALLED_APPS` :
   ```python
   INSTALLED_APPS = [
       ...
       'ckeditor',
       'ckeditor_uploader',
       ...
   ]
   ```
2. Vérifier que les fichiers statiques sont collectés :
   ```bash
   python manage.py collectstatic
   ```
3. Vider le cache du navigateur (Ctrl+Shift+R ou Cmd+Shift+R)
4. Vérifier la console JavaScript du navigateur (F12) pour des erreurs

### L'upload d'images ne fonctionne pas

**Symptôme** : Erreur lors de l'upload ou image non visible après l'upload

**Solutions** :
1. Vérifier les permissions du dossier `media/` :
   ```bash
   # En production (VPS)
   sudo chown -R www-data:www-data /var/www/amcd57/media/
   sudo chmod -R 755 /var/www/amcd57/media/
   ```
2. Vérifier `MEDIA_URL` et `MEDIA_ROOT` dans `settings.py` :
   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```
3. Vérifier la configuration Nginx en production (routes `/media/`)
4. Vérifier la taille du fichier (max 10 MB)

### Images cassées dans les articles

**Symptôme** : Les images affichent une icône "image cassée" sur le frontend

**Solutions** :
1. Vérifier que les fichiers existent dans `media/blog/articles/`
2. Vérifier la configuration Nginx en production :
   ```nginx
   location /media/ {
       alias /var/www/amcd57/media/;
   }
   ```
3. Vérifier les permissions de lecture :
   ```bash
   sudo chmod -R 755 /var/www/amcd57/media/
   ```

### Le formatage ne s'affiche pas correctement sur le site

**Symptôme** : Le contenu HTML n'est pas rendu correctement sur le frontend

**Solutions** :
1. Vérifier que le template utilise `|safe` pour afficher le HTML :
   ```django
   {{ article.contenu|safe }}
   ```
2. Vérifier la CSP (Content Security Policy) dans Nginx si le CSS inline est bloqué
3. Ajouter des styles CSS personnalisés pour les éléments CKEditor si nécessaire

### Après déploiement, CKEditor ne fonctionne plus

**Checklist de déploiement** :
1. ✅ `pip install django-ckeditor==6.7.1` sur le serveur
2. ✅ `python manage.py migrate` (migration 0002)
3. ✅ `python manage.py collectstatic --noinput`
4. ✅ Vérifier les permissions `media/`
5. ✅ Redémarrer Gunicorn : `sudo systemctl restart gunicorn-amcd57`
6. ✅ Recharger Nginx : `sudo systemctl reload nginx`
7. ✅ Tester l'upload d'une image test

---

## 📚 Ressources supplémentaires

### Documentation officielle

- **CKEditor 4** : https://ckeditor.com/docs/ckeditor4/latest/
- **django-ckeditor** : https://github.com/django-ckeditor/django-ckeditor
- **Guide utilisateur CKEditor** : https://ckeditor.com/docs/ckeditor4/latest/guide/

### Tutoriels vidéo

- Recherchez "CKEditor tutorial" sur YouTube pour des tutoriels visuels
- La plupart des concepts s'appliquent à notre configuration

### Support

- **Questions techniques** : Consulter [CLAUDE.md](CLAUDE.md) pour l'architecture du projet
- **Problèmes de déploiement** : Voir [DEPLOIEMENT.md](DEPLOIEMENT.md)
- **Documentation Django** : https://docs.djangoproject.com/

---

## 🎓 Formation rapide (5 minutes)

### Pour les nouveaux utilisateurs

**Exercice 1 : Créer un article simple**
1. Allez dans Admin → Blog → Articles → Ajouter un article
2. Titre : "Article de test"
3. Dans l'éditeur, tapez quelques paragraphes
4. Sélectionnez un mot et mettez-le en **gras**
5. Créez une liste à puces
6. Statut : Brouillon
7. Enregistrez

**Exercice 2 : Ajouter une image**
1. Ouvrez l'article de test
2. Cliquez sur l'icône Image
3. Uploadez une photo (< 2 MB)
4. Ajoutez un texte alternatif : "Photo de test du club"
5. Centrez l'image
6. Enregistrez

**Exercice 3 : Insérer un lien**
1. Tapez "Visitez notre page Facebook"
2. Sélectionnez "page Facebook"
3. Cliquez sur l'icône Link
4. URL : `https://facebook.com/amcd57` (exemple)
5. Target : "_blank"
6. Enregistrez

**Exercice 4 : Publier l'article**
1. Changez le statut de "Brouillon" à "Publié"
2. Enregistrez
3. Visitez le site pour voir votre article en ligne

**🎉 Félicitations ! Vous maîtrisez les bases de CKEditor !**

---

## ✅ Checklist avant publication

Avant de publier un article, vérifiez :

- [ ] Le titre est clair et descriptif
- [ ] Le contenu est structuré avec des titres (H2, H3)
- [ ] Les images ont un texte alternatif (alt)
- [ ] Les images sont optimisées (< 500 KB chacune)
- [ ] Les liens fonctionnent et s'ouvrent correctement
- [ ] L'orthographe et la grammaire sont correctes
- [ ] Le formatage est cohérent (pas d'abus de gras/italique)
- [ ] La catégorie est appropriée
- [ ] Des tags pertinents sont ajoutés
- [ ] L'extrait est pertinent (ou généré automatiquement)
- [ ] Une image à la une est uploadée
- [ ] Le statut est bien sur "Publié"
- [ ] Aperçu de l'article sur le site avant de le rendre public

---

**Document créé le** : 29 octobre 2025
**Dernière mise à jour** : 29 octobre 2025
**Version** : 1.0
**Auteur** : Équipe AMCD57

*Ce guide sera mis à jour régulièrement avec de nouveaux conseils et astuces basés sur l'utilisation réelle.*
