# 🚀 Configuration Production AMCD57

## 📋 Vue d'ensemble

Ce document décrit la configuration de production complète du site AMCD57 déployé sur VPS OVH.

- **URL** : https://amcd.alodev.ovh
- **Serveur** : VPS OVH Ubuntu 25.04
- **Utilisateur système** : `amcd`
- **Répertoire application** : `/var/www/amcd57`
- **Stack** : Django 5.0 + Gunicorn + Nginx + PostgreSQL (ou SQLite)
- **SSL** : Let's Encrypt (Certbot)

---

## 🔧 Variables d'environnement (.env)

Fichier : `/var/www/amcd57/.env`

```env
# Django Core
SECRET_KEY=<votre-secret-key-généré>
DEBUG=False
ALLOWED_HOSTS=amcd.alodev.ovh,www.amcd.alodev.ovh,localhost,127.0.0.1

# Media Files (IMPORTANT)
MEDIA_ROOT=/var/www/amcd57/media
MEDIA_URL=/media/

# OpenWeather API
OPENWEATHER_API_KEY=<votre-clé-api>

# Email (optionnel - à configurer si nécessaire)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=email@example.com
# EMAIL_HOST_PASSWORD=password
# EMAIL_USE_TLS=True

# Database (si PostgreSQL utilisé)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Variables critiques à vérifier

| Variable | Valeur Production | Remarque |
|----------|------------------|----------|
| `DEBUG` | `False` | **OBLIGATOIRE** en production |
| `MEDIA_ROOT` | `/var/www/amcd57/media` | Corrige le problème d'upload photos |
| `MEDIA_URL` | `/media/` | URL publique des médias |
| `ALLOWED_HOSTS` | Domaine(s) du site | Séparés par des virgules |

---

## ⚙️ Configuration Gunicorn

Fichier : `/var/www/amcd57/gunicorn_config.py`

### Paramètres clés

```python
# Écoute sur localhost uniquement (Nginx fait le reverse proxy)
bind = '127.0.0.1:8000'

# Workers (2 × CPU cores) + 1
workers = 9

# Logs
accesslog = '/var/www/amcd57/logs/gunicorn-access.log'
errorlog = '/var/www/amcd57/logs/gunicorn-error.log'
loglevel = 'info'

# Répertoire temporaire (IMPORTANT - résout le problème de permissions)
worker_tmp_dir = '/var/www/amcd57/tmp'

# User/Group - COMMENTÉ pour éviter les problèmes de permissions
# user = 'amcd'
# group = 'amcd'
```

### ⚠️ Corrections appliquées

1. **`worker_tmp_dir`** : Ajouté pour éviter les erreurs de permissions sur `/tmp/`
2. **`user` et `group`** : Commentés car causaient `PermissionError` au démarrage

---

## 🌐 Configuration Nginx

Fichier : `/etc/nginx/sites-available/amcd57`

### Section Media Files (critique)

```nginx
# Servir les fichiers média
location /media/ {
    alias /var/www/amcd57/media/;  # IMPORTANT : pointe vers media/, pas mediafiles/
    expires 30d;
    add_header Cache-Control "public";
}

# Servir les fichiers statiques
location /static/ {
    alias /var/www/amcd57/staticfiles/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# Reverse proxy vers Gunicorn
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Vérification Nginx

```bash
# Tester la configuration
sudo nginx -t

# Recharger Nginx après modification
sudo systemctl reload nginx

# Redémarrer Nginx si nécessaire
sudo systemctl restart nginx
```

---

## 📂 Structure des répertoires

```
/var/www/amcd57/
├── amcd57_project/          # Projet Django
│   ├── settings.py          # Settings avec config() pour .env
│   ├── urls.py
│   └── wsgi.py
├── blog/                    # App Blog
├── core/                    # App Core
├── events/                  # App Events
├── members/                 # App Members
├── weblinks/                # App Weblinks
├── media/                   # ✅ MÉDIA (uploads utilisateurs)
│   ├── blog/
│   ├── events/
│   ├── members/
│   │   └── photos/          # Photos de profil
│   └── weblinks/
├── mediafiles/              # ⚠️  Ancien répertoire (à supprimer après migration)
├── staticfiles/             # Fichiers statiques collectés
├── templates/               # Templates globaux
├── static/                  # Fichiers statiques sources
├── logs/                    # Logs Gunicorn
│   ├── gunicorn-access.log
│   └── gunicorn-error.log
├── tmp/                     # Répertoire temporaire Gunicorn
├── venv/                    # Environnement virtuel Python
├── manage.py
├── requirements.txt
├── gunicorn_config.py
└── .env                     # Variables d'environnement
```

---

## 🗄️ Base de données

### Type de base utilisée

- **Développement** : SQLite (`db.sqlite3`)
- **Production** : SQLite (peut être migrée vers PostgreSQL ultérieurement)

### Commandes importantes

```bash
# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Exporter les données (backup)
python manage.py dumpdata \
  --exclude auth.permission \
  --exclude contenttypes \
  --exclude admin.logentry \
  --indent 2 \
  > backup_$(date +%Y%m%d_%H%M%S).json

# Importer les données
python manage.py loaddata backup.json
```

---

## 🔐 Permissions

### Propriétaire des fichiers

```bash
# Tous les fichiers doivent appartenir à l'utilisateur amcd
sudo chown -R amcd:amcd /var/www/amcd57/

# Permissions media (lecture/écriture pour upload)
sudo chmod -R 755 /var/www/amcd57/media/

# Permissions tmp (nécessaire pour Gunicorn)
sudo chmod 755 /var/www/amcd57/tmp/
```

### Vérification

```bash
# Vérifier les permissions
ls -la /var/www/amcd57/ | grep -E "media|tmp|logs"

# Test d'écriture dans media
echo "test" > /var/www/amcd57/media/members/photos/test.txt && rm /var/www/amcd57/media/members/photos/test.txt && echo "✅ Écriture OK"
```

---

## 🔄 Commandes de maintenance

### Redémarrer les services

```bash
# Redémarrer Gunicorn
sudo systemctl restart gunicorn-amcd57

# Redémarrer Nginx
sudo systemctl restart nginx

# Vérifier le statut
sudo systemctl status gunicorn-amcd57
sudo systemctl status nginx
```

### Voir les logs

```bash
# Logs Gunicorn en temps réel
sudo journalctl -u gunicorn-amcd57 -f

# Logs d'erreur Gunicorn
tail -f /var/www/amcd57/logs/gunicorn-error.log

# Logs d'accès Gunicorn
tail -f /var/www/amcd57/logs/gunicorn-access.log

# Logs Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Collecter les fichiers statiques

```bash
cd /var/www/amcd57
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-amcd57
```

---

## 🚀 Procédure de déploiement

### Mise à jour du code

```bash
# 1. SSH sur le VPS
ssh alodev.ovh

# 2. Aller dans le répertoire
cd /var/www/amcd57

# 3. Pull les changements
git pull

# 4. Activer l'environnement virtuel
source venv/bin/activate

# 5. Installer les nouvelles dépendances (si requirements.txt modifié)
pip install -r requirements.txt

# 6. Appliquer les migrations
python manage.py migrate

# 7. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 8. Redémarrer Gunicorn
sudo systemctl restart gunicorn-amcd57

# 9. Vérifier que tout fonctionne
sudo systemctl status gunicorn-amcd57
```

### Vérifications post-déploiement

```bash
# 1. Vérifier que le site est accessible
curl -I https://amcd.alodev.ovh

# 2. Vérifier les logs pour des erreurs
sudo journalctl -u gunicorn-amcd57 -n 20 --no-pager

# 3. Tester l'admin Django
# Aller sur https://amcd.alodev.ovh/admin/ et se connecter

# 4. Tester l'upload de photo
# Aller sur https://amcd.alodev.ovh/membres/profil/modifier/
```

---

## 🐛 Problèmes résolus (historique)

### 1. Photos sauvegardées dans `mediafiles/` au lieu de `media/`

**Symptôme** : Upload de photo réussit mais fichiers n'apparaissent pas sur le site.

**Cause** : `MEDIA_ROOT` défini en dur dans `settings.py` production :
```python
# ❌ Ancienne version (problématique)
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
```

**Solution** :
1. Modifier `settings.py` pour lire depuis `.env` :
   ```python
   # ✅ Nouvelle version (correcte)
   MEDIA_ROOT = config('MEDIA_ROOT', default=str(BASE_DIR / 'media'))
   ```
2. Ajouter dans `.env` :
   ```env
   MEDIA_ROOT=/var/www/amcd57/media
   ```
3. Copier les fichiers de `mediafiles/` vers `media/` :
   ```bash
   cp -r /var/www/amcd57/mediafiles/* /var/www/amcd57/media/
   ```
4. Mettre à jour Nginx pour servir depuis `media/`

**Fichiers concernés** :
- `amcd57_project/settings.py`
- `/var/www/amcd57/.env`
- `/etc/nginx/sites-available/amcd57`

---

### 2. Gunicorn ne démarre pas : PermissionError sur `/tmp/`

**Symptôme** : Gunicorn crashe avec :
```
PermissionError: [Errno 1] Operation not permitted: '/tmp/wgunicorn-...'
```

**Cause** : Configuration `user` et `group` dans `gunicorn_config.py` causait des problèmes de permissions.

**Solution** :
1. Ajouter `worker_tmp_dir` dans `gunicorn_config.py` :
   ```python
   worker_tmp_dir = '/var/www/amcd57/tmp'
   ```
2. Créer le répertoire avec bonnes permissions :
   ```bash
   mkdir -p /var/www/amcd57/tmp
   chmod 755 /var/www/amcd57/tmp
   ```
3. Commenter les lignes `user` et `group` dans `gunicorn_config.py` :
   ```python
   # user = 'amcd'
   # group = 'amcd'
   ```

**Fichier concerné** :
- `gunicorn_config.py`

---

### 3. Erreur 400 Bad Request après git reset

**Symptôme** : Site affiche "Bad Request (400)"

**Cause** : `ALLOWED_HOSTS` réinitialisé à `['localhost', '127.0.0.1']`

**Solution** : Configurer `ALLOWED_HOSTS` via `.env` :
```python
# settings.py
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```
```env
# .env
ALLOWED_HOSTS=amcd.alodev.ovh,www.amcd.alodev.ovh,localhost,127.0.0.1
```

---

### 4. Erreur 500 : no such table: django_session

**Symptôme** : Site affiche "Server Error (500)" avec `no such table: django_session`

**Cause** : Migrations non appliquées après `git reset --hard`

**Solution** :
```bash
python manage.py migrate
sudo systemctl restart gunicorn-amcd57
```

---

### 5. Perte des données après réinitialisation BDD

**Symptôme** : Tous les articles, événements, membres ont disparu

**Cause** : `git reset --hard` a réinitialisé la base de données

**Solution** : Réimporter depuis backup JSON :
```bash
python manage.py loaddata backup.json
```

---

## 📊 Checklist de santé du serveur

### Vérifications quotidiennes

- [ ] Site accessible : https://amcd.alodev.ovh
- [ ] Admin accessible : https://amcd.alodev.ovh/admin/
- [ ] Certificat SSL valide (renouvellement auto Certbot)
- [ ] Espace disque disponible : `df -h`
- [ ] Services actifs :
  - [ ] `sudo systemctl status gunicorn-amcd57`
  - [ ] `sudo systemctl status nginx`

### Vérifications hebdomadaires

- [ ] Backup de la base de données
- [ ] Backup du répertoire `media/`
- [ ] Logs sans erreurs critiques
- [ ] Mises à jour système disponibles : `sudo apt update && sudo apt list --upgradable`

### Vérifications mensuelles

- [ ] Mise à jour des dépendances Python : `pip list --outdated`
- [ ] Vérification de la sécurité : `python manage.py check --deploy`
- [ ] Rotation des logs
- [ ] Test de restauration backup

---

## 🔗 Liens utiles

- **Site en ligne** : https://amcd.alodev.ovh
- **Admin Django** : https://amcd.alodev.ovh/admin/
- **Repository Git** : https://github.com/alo635/amcd57-django
- **Documentation Django** : https://docs.djangoproject.com/fr/5.0/

---

## 📞 Contacts et support

### En cas de problème

1. **Consulter les logs** :
   ```bash
   sudo journalctl -u gunicorn-amcd57 -n 50 --no-pager
   ```

2. **Vérifier la documentation** :
   - [DEPLOIEMENT.md](DEPLOIEMENT.md) - Guide de déploiement complet
   - [DEBUG_PHOTO_UPLOAD.md](DEBUG_PHOTO_UPLOAD.md) - Problèmes d'upload photos
   - [GUIDE_DEBUG_PHOTO_PRODUCTION.md](GUIDE_DEBUG_PHOTO_PRODUCTION.md) - Debug production

3. **Scripts de diagnostic** :
   ```bash
   sudo bash /var/www/amcd57/scripts/diagnostic_photo_production.sh
   ```

### Informations système

```bash
# Version Python
python3 --version

# Version Django
python -c "import django; print(django.get_version())"

# Version Gunicorn
gunicorn --version

# Version Nginx
nginx -v

# Version Ubuntu
lsb_release -a
```

---

## 🎯 Statut actuel

✅ **Site opérationnel à 100%**

- ✅ Toutes les fonctionnalités testées et validées
- ✅ Upload de photos fonctionne correctement
- ✅ Base de données migrée et fonctionnelle
- ✅ SSL/HTTPS configuré
- ✅ Nginx + Gunicorn configurés
- ✅ Logs accessibles et propres
- ✅ Permissions correctes
- ✅ Variables d'environnement configurées

**Dernière mise à jour** : 26 octobre 2025
**Version Django** : 5.0
**Version Python** : 3.13.3

---

*Document généré avec Claude Code - Projet AMCD57*
