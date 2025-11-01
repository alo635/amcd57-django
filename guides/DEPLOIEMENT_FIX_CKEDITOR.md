# 🚀 Déploiement - Correction CKEditor Path

## Contexte

Correction du bug de chemin d'upload CKEditor qui créait des dossiers `%Y/%m/username/`
au lieu de `YYYY/MM/`.

**Commits concernés** :
- `9b5285b` - fix: Correction chemin d'upload CKEditor
- `1259aca` - docs: Ajout documentation complète CKEditor

---

## 📋 Checklist de déploiement

- [ ] Se connecter au VPS
- [ ] Naviguer vers le projet
- [ ] Activer l'environnement virtuel
- [ ] Pull les changements depuis GitHub
- [ ] Vérifier la configuration settings.py
- [ ] Vérifier l'existence de dossiers incorrects
- [ ] Nettoyer les dossiers incorrects si nécessaire
- [ ] Redémarrer Gunicorn
- [ ] Tester l'upload d'une image
- [ ] Vérifier que le chemin est correct

---

## 🔧 Commandes de déploiement

### 1. Connexion au VPS

```bash
ssh amcd@VPS_IP
```

### 2. Navigation et activation venv

```bash
cd /var/www/amcd57
source venv/bin/activate
```

### 3. Pull les changements depuis GitHub

```bash
git pull origin main
```

**Résultat attendu** :
```
From https://github.com/alo635/amcd57-django
 * branch            main       -> FETCH_HEAD
Updating 1259aca..9b5285b
Fast-forward
 amcd57_project/settings.py | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)
```

### 4. Vérifier le changement dans settings.py

```bash
grep -A 2 "CKEDITOR_RESTRICT_BY_USER" amcd57_project/settings.py
```

**Résultat attendu** :
```python
# Ne pas restreindre par utilisateur (tous les membres du club peuvent voir toutes les images)
CKEDITOR_RESTRICT_BY_USER = False  # Si True, ajoute username au path
CKEDITOR_BROWSE_SHOW_DIRS = True  # Montrer les dossiers dans le browser
```

### 5. Vérifier la structure des dossiers media

```bash
find media/blog/articles -type d | sort
```

**Vérifier s'il existe des dossiers comme** :
- `media/blog/articles/%Y/`
- `media/blog/articles/%Y/%m/`
- Ou des dossiers avec des usernames

### 6. Nettoyer les dossiers incorrects (si nécessaire)

**Si des dossiers incorrects existent** :

```bash
# D'abord, chercher s'il y a des fichiers dedans
find media/blog/articles/%Y -type f 2>/dev/null

# Si des fichiers existent, les déplacer (adapter la date selon vos besoins)
mkdir -p media/blog/articles/2025/10
mv media/blog/articles/%Y/%m/*/2025/10/29/*.png media/blog/articles/2025/10/ 2>/dev/null
mv media/blog/articles/%Y/%m/*/2025/10/*.png media/blog/articles/2025/10/ 2>/dev/null

# Vérifier que les fichiers ont été déplacés
ls -la media/blog/articles/2025/10/

# Supprimer le dossier incorrect
rm -rf media/blog/articles/%Y
```

**Si aucun dossier incorrect n'existe**, passez à l'étape suivante.

### 7. Vérifier les permissions

```bash
# S'assurer que www-data a les bonnes permissions sur media/
sudo chown -R www-data:www-data /var/www/amcd57/media/
sudo chmod -R 755 /var/www/amcd57/media/
```

### 8. Redémarrer Gunicorn

```bash
sudo systemctl restart gunicorn-amcd57
```

### 9. Vérifier le statut de Gunicorn

```bash
sudo systemctl status gunicorn-amcd57
```

**Résultat attendu** :
```
● gunicorn-amcd57.service - Gunicorn daemon for AMCD57 Django project
     Loaded: loaded
     Active: active (running) since ...
```

### 10. Vérifier les logs Gunicorn

```bash
sudo journalctl -u gunicorn-amcd57 -n 20 --no-pager
```

**Vérifier qu'il n'y a pas d'erreurs.**

---

## 🧪 Test en production

### 1. Se connecter à l'admin

Aller sur : `https://amcd.alodev.ovh/admin/`

### 2. Ouvrir un article existant ou en créer un nouveau

**Blog → Articles → Ajouter un article** (ou modifier un existant)

### 3. Uploader une image dans CKEditor

1. Cliquer sur l'icône **Image** dans la toolbar
2. Onglet **Upload**
3. Choisir une image (< 2 MB)
4. Cliquer sur **Send it to the Server**
5. L'image devrait s'uploader avec succès

### 4. Vérifier le chemin d'upload

De retour sur le VPS :

```bash
# Voir les derniers fichiers uploadés
find media/blog/articles -type f -name "*.png" -o -name "*.jpg" | tail -5

# Le chemin devrait être : media/blog/articles/2025/10/nom-image.png
# PAS : media/blog/articles/%Y/%m/username/2025/10/nom-image.png
```

### 5. Vérifier l'affichage sur le frontend

1. Sauvegarder l'article avec statut **Publié**
2. Aller sur le blog : `https://amcd.alodev.ovh/blog/`
3. Ouvrir l'article
4. Vérifier que l'image s'affiche correctement

---

## ✅ Validation du déploiement

Cochez les éléments suivants :

- [ ] Git pull réussi sans conflit
- [ ] `CKEDITOR_RESTRICT_BY_USER = False` dans settings.py
- [ ] Aucun dossier `%Y/` ou `%m/` dans media/blog/articles/
- [ ] Permissions correctes sur media/ (www-data:www-data, 755)
- [ ] Gunicorn redémarré et actif
- [ ] Aucune erreur dans les logs Gunicorn
- [ ] Upload d'image test réussi
- [ ] Chemin d'upload correct : `media/blog/articles/YYYY/MM/image.ext`
- [ ] Image visible dans l'admin CKEditor
- [ ] Image visible sur le frontend du site

---

## 🐛 Dépannage

### Problème : Git pull échoue avec des conflits

**Solution** :
```bash
# Voir les fichiers en conflit
git status

# Si settings.py est en conflit et que vous voulez garder la version GitHub
git checkout origin/main -- amcd57_project/settings.py

# Ou stash les changements locaux
git stash
git pull origin main
```

### Problème : Gunicorn ne redémarre pas

**Solution** :
```bash
# Voir les logs d'erreur détaillés
sudo journalctl -u gunicorn-amcd57 -n 50

# Vérifier la syntaxe Python
cd /var/www/amcd57
source venv/bin/activate
python manage.py check

# Redémarrer manuellement
sudo systemctl stop gunicorn-amcd57
sudo systemctl start gunicorn-amcd57
```

### Problème : Image n'est pas visible après upload

**Vérifications** :
```bash
# 1. Vérifier que le fichier existe
ls -la media/blog/articles/2025/10/

# 2. Vérifier les permissions
ls -la media/blog/articles/2025/10/*.png

# 3. Corriger les permissions si nécessaire
sudo chown www-data:www-data media/blog/articles/2025/10/*.png
sudo chmod 644 media/blog/articles/2025/10/*.png

# 4. Vérifier la config Nginx pour /media/
sudo cat /etc/nginx/sites-available/amcd57 | grep -A 5 "location /media"
```

### Problème : Les anciens articles montrent toujours le mauvais chemin

**Explication** : Les articles créés avant la correction ont des chemins hardcodés dans le HTML.

**Solutions** :
1. **Manuel** : Éditer chaque article et re-uploader l'image
2. **Script SQL** (plus rapide) :
   ```bash
   # Se connecter à PostgreSQL
   sudo -u postgres psql amcd57_db

   # Voir les articles concernés
   SELECT id, titre, contenu FROM blog_article WHERE contenu LIKE '%/%Y/%m/%';

   # Remplacer les chemins (adapter selon vos besoins)
   UPDATE blog_article
   SET contenu = REPLACE(contenu, '/media/blog/articles/%Y/%m/alex/2025/10/29/', '/media/blog/articles/2025/10/')
   WHERE contenu LIKE '%/%Y/%m/%';

   # Vérifier le résultat
   SELECT id, titre FROM blog_article WHERE contenu LIKE '%/%Y/%m/%';

   # Quitter
   \q
   ```

---

## 📝 Notes importantes

1. **Backup** : Un backup automatique de la DB est fait chaque nuit à 2h00. Les fichiers media sont backupés à 3h00.

2. **Pas de downtime** : Gunicorn redémarre sans interruption de service (graceful restart).

3. **Cache Nginx** : Si les images ne se mettent pas à jour, vider le cache navigateur (Ctrl+Shift+R).

4. **Futurs uploads** : Tous les uploads futurs utiliseront automatiquement le bon format de chemin.

---

## 📊 Résultat attendu

**Avant** :
```
media/blog/articles/%Y/%m/alex/2025/10/29/image.png
```

**Après** :
```
media/blog/articles/2025/10/image.png
```

**Structure finale attendue** :
```
media/blog/articles/
├── 2020/
│   ├── 01/
│   ├── 02/
│   └── 11/
├── 2022/
│   └── 09/
└── 2025/
    └── 10/
        ├── image1.png
        ├── image2.jpg
        └── ...
```

---

**Dernière mise à jour** : 29 octobre 2025
**Durée estimée** : 5-10 minutes
**Difficulté** : Facile ⭐
