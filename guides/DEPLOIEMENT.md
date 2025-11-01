# 🚀 Guide de Déploiement AMCD57 sur VPS OVH

Guide complet pour déployer le site Django AMCD57 sur un VPS OVH Ubuntu 25.04.

---

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Configuration DNS](#configuration-dns)
3. [Connexion et sécurisation du serveur](#connexion-et-sécurisation-du-serveur)
4. [Installation des dépendances système](#installation-des-dépendances-système)
5. [Configuration PostgreSQL](#configuration-postgresql)
6. [Déploiement de l'application Django](#déploiement-de-lapplication-django)
7. [Configuration Gunicorn](#configuration-gunicorn)
8. [Configuration Nginx](#configuration-nginx)
9. [Configuration SSL avec Certbot](#configuration-ssl-avec-certbot)
10. [Configuration des fichiers statiques et médias](#configuration-des-fichiers-statiques-et-médias)
11. [Variables d'environnement de production](#variables-denvironnement-de-production)
12. [Mise en place des sauvegardes](#mise-en-place-des-sauvegardes)
13. [Monitoring et logs](#monitoring-et-logs)
14. [Migration vers le domaine définitif](#migration-vers-le-domaine-définitif)
15. [Checklist finale](#checklist-finale)

---

## 🎯 Prérequis

### Informations nécessaires
- ✅ VPS OVH avec Ubuntu 25.04
- ✅ Accès root via SSH
- ✅ Domaine temporaire : `amcd.alodev.ovh`
- ✅ Domaine définitif : `www.amcd57.fr`
- ⚠️ Email administrateur (pour SSL et notifications)
- ⚠️ Clé API OpenWeatherMap
- ⚠️ Identifiants SMTP (Gmail, SendGrid, etc.)

### Sur votre machine locale
```bash
# Vérifier que le projet est à jour
git status
git pull

# Tester localement une dernière fois
source venv/bin/activate
python manage.py test
python manage.py check --deploy
```

---

## 🌐 Configuration DNS

### 1. Configuration chez OVH

Connectez-vous à votre espace client OVH et configurez les enregistrements DNS pour `amcd.alodev.ovh` :

```
Type    Sous-domaine    Cible                 TTL
A       amcd            <IP_VPS_OVH>          3600
CNAME   www.amcd        amcd.alodev.ovh.      3600
```

### 2. Vérification DNS

```bash
# Attendre la propagation DNS (peut prendre jusqu'à 24h)
# Vérifier la propagation
dig amcd.alodev.ovh
nslookup amcd.alodev.ovh

# Devrait retourner l'IP de votre VPS
ping amcd.alodev.ovh
```

---

## 🔐 Connexion et sécurisation du serveur

### 1. Première connexion

```bash
# Se connecter au VPS (remplacer IP_VPS par votre IP)
ssh root@<IP_VPS_OVH>
```

### 2. Mise à jour du système

```bash
# Mettre à jour les paquets
apt update && apt upgrade -y

# Installer les utilitaires de base
apt install -y curl wget git vim ufw build-essential software-properties-common
```

### 3. Créer un utilisateur non-root

```bash
# Créer l'utilisateur 'amcd' (ou votre nom)
adduser amcd

# Donner les droits sudo
usermod -aG sudo amcd

# Configurer SSH pour cet utilisateur
mkdir -p /home/amcd/.ssh
cp ~/.ssh/authorized_keys /home/amcd/.ssh/
chown -R amcd:amcd /home/amcd/.ssh
chmod 700 /home/amcd/.ssh
chmod 600 /home/amcd/.ssh/authorized_keys
```

### 4. Configurer le pare-feu UFW

```bash
# Autoriser SSH
ufw allow OpenSSH

# Autoriser HTTP et HTTPS
ufw allow 'Nginx Full'

# Activer le pare-feu
ufw enable

# Vérifier le statut
ufw status
```

### 5. Sécuriser SSH

```bash
# Éditer la configuration SSH
vim /etc/ssh/sshd_config

# Modifier ces lignes :
# PermitRootLogin no
# PasswordAuthentication no
# PubkeyAuthentication yes

# Redémarrer SSH
systemctl restart sshd
```

### 6. Se reconnecter avec le nouvel utilisateur

```bash
# Depuis votre machine locale
ssh amcd@<IP_VPS_OVH>
```

---

## 📦 Installation des dépendances système

### 1. Installer Python 3.13

```bash
# Ajouter le PPA deadsnakes pour Python 3.13
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Installer Python 3.13
sudo apt install -y python3.13 python3.13-venv python3.13-dev

# Vérifier l'installation
python3.13 --version
```

### 2. Installer PostgreSQL

```bash
# Installer PostgreSQL 16 (dernière version stable)
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Vérifier que PostgreSQL est démarré
sudo systemctl status postgresql
sudo systemctl enable postgresql
```

### 3. Installer Nginx

```bash
# Installer Nginx
sudo apt install -y nginx

# Démarrer et activer Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Vérifier le statut
sudo systemctl status nginx
```

### 4. Installer les dépendances pour Pillow

```bash
# Installer les bibliothèques nécessaires pour Pillow
sudo apt install -y libjpeg-dev zlib1g-dev libpng-dev
```

---

## 🗄️ Configuration PostgreSQL

### 1. Créer la base de données et l'utilisateur

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans le shell PostgreSQL :
CREATE DATABASE amcd57_db;
CREATE USER amcd57_user WITH PASSWORD 'VOTRE_MOT_DE_PASSE_SECURISE';

-- Configurer les droits
ALTER ROLE amcd57_user SET client_encoding TO 'utf8';
ALTER ROLE amcd57_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE amcd57_user SET timezone TO 'Europe/Paris';
GRANT ALL PRIVILEGES ON DATABASE amcd57_db TO amcd57_user;

-- Quitter
\q
```

### 2. ⚠️ IMPORTANT : Configurer les permissions sur le schéma public (PostgreSQL 15+)

**Depuis PostgreSQL 15, les permissions par défaut ont changé.** Il faut explicitement accorder les droits sur le schéma `public` :

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Se connecter à la base de données
\c amcd57_db

# Accorder tous les privilèges sur le schéma public
GRANT ALL ON SCHEMA public TO amcd57_user;
GRANT CREATE ON SCHEMA public TO amcd57_user;

-- Faire de amcd57_user le propriétaire du schéma (recommandé)
ALTER SCHEMA public OWNER TO amcd57_user;

-- Définir les privilèges par défaut pour les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO amcd57_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO amcd57_user;

-- Vérifier les permissions
\dn+

-- Quitter
\q
```

**Note** : Sans cette étape, vous obtiendrez l'erreur `permission denied for schema public` lors de `python manage.py migrate`.

### 3. Tester la connexion

```bash
# Tester la connexion à la base
psql -U amcd57_user -d amcd57_db -h localhost
# Entrer le mot de passe
# Si ça fonctionne, taper \q pour quitter
```

### 4. Configuration PostgreSQL pour connexions locales

```bash
# Éditer pg_hba.conf
sudo vim /etc/postgresql/16/main/pg_hba.conf

# Ajouter/modifier cette ligne (si pas déjà présente) :
# local   all             all                                     md5

# Redémarrer PostgreSQL
sudo systemctl restart postgresql
```

---

## 🐍 Déploiement de l'application Django

### 1. Créer la structure des répertoires

```bash
# Créer le répertoire pour l'application
sudo mkdir -p /var/www/amcd57
sudo chown -R amcd:amcd /var/www/amcd57

# Se positionner dans le répertoire
cd /var/www/amcd57
```

### 2. Cloner le repository

```bash
# Cloner depuis GitHub
git clone https://github.com/alo635/amcd57-django.git .

# Ou si vous utilisez SSH
# git clone git@github.com:alo635/amcd57-django.git .

# Vérifier le contenu
ls -la
```

### 3. Créer l'environnement virtuel

```bash
# Créer l'environnement virtuel avec Python 3.13
python3.13 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier la version de Python
python --version
# Doit afficher : Python 3.13.x
```

### 4. Installer les dépendances Python

```bash
# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances du projet
pip install -r requirements.txt

# Installer psycopg2 pour PostgreSQL
pip install psycopg2-binary

# Installer gunicorn
pip install gunicorn
```

### 5. Créer les répertoires media et staticfiles

```bash
# Créer les répertoires nécessaires
mkdir -p /var/www/amcd57/media/blog/articles
mkdir -p /var/www/amcd57/media/blog/categories
mkdir -p /var/www/amcd57/media/events/evenements
mkdir -p /var/www/amcd57/media/members/profils
mkdir -p /var/www/amcd57/media/weblinks/liens
mkdir -p /var/www/amcd57/staticfiles
mkdir -p /var/www/amcd57/logs

# Définir les permissions
chmod -R 755 /var/www/amcd57/media
chmod -R 755 /var/www/amcd57/staticfiles
chmod -R 755 /var/www/amcd57/logs
```

### 6. Créer le fichier .env de production

```bash
# Créer le fichier .env
vim .env
```

Contenu du fichier `.env` :

```env
# Django Core
SECRET_KEY=GENERER_UNE_NOUVELLE_CLE_SECRETE_LONGUE_ET_COMPLEXE
DEBUG=False
ALLOWED_HOSTS=amcd.alodev.ovh,www.amcd.alodev.ovh,localhost,127.0.0.1,<IP_VPS>

# Database
DATABASE_URL=postgresql://amcd57_user:VOTRE_MOT_DE_PASSE_SECURISE@localhost:5432/amcd57_db
DB_PASSWORD=VOTRE_MOT_DE_PASSE_SECURISE

# Email Configuration (exemple avec Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre.email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_application

# OpenWeatherMap API
OPENWEATHER_API_KEY=votre_cle_api_openweathermap

# Sécurité (⚠️ DÉSACTIVÉ INITIALEMENT - Réactiver après SSL)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
```

**⚠️ IMPORTANT** : Les paramètres de sécurité HTTPS sont désactivés (`False`) initialement. Vous les réactiverez (`True`) **APRÈS** l'installation du certificat SSL avec Certbot. Si vous les activez avant, le site ne sera pas accessible en HTTP.

**Important** : Pour générer une SECRET_KEY sécurisée :

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 6. Configurer settings.py pour la production

```bash
# Éditer settings.py
vim amcd57_project/settings.py
```

Ajouter/modifier ces lignes dans `settings.py` :

```python
import os
from decouple import config, Csv

# ... (garder les imports existants)

# Database avec support PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='amcd57_db'),
        'USER': config('DB_USER', default='amcd57_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Allowed Hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Static et Media en production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Sécurité
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
```

### 7. Effectuer les migrations

```bash
# Effectuer les migrations (⚠️ AVANT collectstatic)
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
# Suivre les instructions (email + mot de passe)

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

### 8. Vérifier que tout fonctionne

```bash
# Test du serveur de développement (temporaire)
python manage.py runserver 0.0.0.0:8000

# Depuis votre navigateur, tester :
# http://<IP_VPS>:8000

# Si vous obtenez "DisallowedHost", vérifiez que l'IP est dans ALLOWED_HOSTS du .env

# Si ça fonctionne, arrêter avec Ctrl+C
```

---

## 🦄 Configuration Gunicorn

### 1. Tester Gunicorn

```bash
# Depuis /var/www/amcd57 avec venv activé
cd /var/www/amcd57
source venv/bin/activate

# Tester Gunicorn
gunicorn --bind 0.0.0.0:8000 amcd57_project.wsgi:application

# Si ça fonctionne, arrêter avec Ctrl+C
```

### 2. Créer le fichier de configuration Gunicorn

```bash
# Créer le fichier gunicorn_config.py
vim gunicorn_config.py
```

Contenu de `gunicorn_config.py` :

```python
"""
Configuration Gunicorn pour AMCD57
"""

import multiprocessing

# Bind
bind = "127.0.0.1:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/www/amcd57/logs/gunicorn-access.log"
errorlog = "/var/www/amcd57/logs/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "amcd57_gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/www/amcd57/gunicorn.pid"
# ⚠️ NE PAS DÉFINIR user/group ici car géré par systemd
# user = "amcd"
# group = "amcd"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
```

**⚠️ NOTE IMPORTANTE** : Les lignes `user` et `group` sont commentées car l'utilisateur est déjà défini dans le fichier service systemd. Si Gunicorn essaie de changer d'utilisateur alors qu'il tourne déjà sous cet utilisateur via systemd, cela causera une erreur.

### 3. Créer le répertoire des logs

```bash
mkdir -p /var/www/amcd57/logs
chmod -R 775 /var/www/amcd57/logs
```

### 4. Créer le service systemd pour Gunicorn

```bash
# Créer le fichier service
sudo vim /etc/systemd/system/gunicorn-amcd57.service
```

Contenu du fichier service :

```ini
[Unit]
Description=Gunicorn daemon for AMCD57 Django application
After=network.target

[Service]
Type=notify
User=amcd
Group=www-data
WorkingDirectory=/var/www/amcd57
Environment="PATH=/var/www/amcd57/venv/bin"
EnvironmentFile=/var/www/amcd57/.env
ExecStart=/var/www/amcd57/venv/bin/gunicorn \
          --config /var/www/amcd57/gunicorn_config.py \
          amcd57_project.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**⚠️ NOTE** : La ligne `EnvironmentFile=/var/www/amcd57/.env` est **essentielle** pour charger les variables d'environnement (SECRET_KEY, DATABASE_URL, etc.) depuis le fichier `.env`.

### 5. Activer et démarrer Gunicorn

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer le service au démarrage
sudo systemctl enable gunicorn-amcd57

# Démarrer le service
sudo systemctl start gunicorn-amcd57

# Vérifier le statut
sudo systemctl status gunicorn-amcd57

# Voir les logs en temps réel
sudo journalctl -u gunicorn-amcd57 -f
```

**⚠️ DÉPANNAGE** : Si Gunicorn ne démarre pas, vérifiez :

```bash
# Voir les erreurs détaillées
sudo journalctl -u gunicorn-amcd57 -n 100 --no-pager

# Problème fréquent : erreur "Can't switch to 'amcd' user"
# → Vérifiez que les lignes user/group sont bien commentées dans gunicorn_config.py

# Problème fréquent : variables d'environnement non chargées
# → Vérifiez que EnvironmentFile=/var/www/amcd57/.env est bien dans le fichier service

# Tester Gunicorn manuellement
cd /var/www/amcd57
source venv/bin/activate
gunicorn --bind 127.0.0.1:8000 amcd57_project.wsgi:application
```

### 6. Commandes utiles pour Gunicorn

```bash
# Démarrer
sudo systemctl start gunicorn-amcd57

# Arrêter
sudo systemctl stop gunicorn-amcd57

# Redémarrer
sudo systemctl restart gunicorn-amcd57

# Recharger (sans downtime)
sudo systemctl reload gunicorn-amcd57

# Voir les logs
sudo journalctl -u gunicorn-amcd57 -n 50
```

---

## 🌐 Configuration Nginx

### 1. Créer la configuration Nginx pour le site

```bash
# Créer le fichier de configuration
sudo vim /etc/nginx/sites-available/amcd57
```

Contenu de `/etc/nginx/sites-available/amcd57` :

```nginx
# Configuration Nginx pour AMCD57
# Domaine temporaire : amcd.alodev.ovh

upstream amcd57_app {
    server 127.0.0.1:8000 fail_timeout=0;
}

# Redirection HTTP vers HTTPS (sera activé après SSL)
server {
    listen 80;
    listen [::]:80;
    server_name amcd.alodev.ovh www.amcd.alodev.ovh;

    # Temporairement, on accepte HTTP
    # Plus tard, on redirigera vers HTTPS
    # return 301 https://$server_name$request_uri;

    # Configuration temporaire (avant SSL)
    location / {
        proxy_pass http://amcd57_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /var/www/amcd57/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/amcd57/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Sécurité : empêcher l'accès aux fichiers cachés
    location ~ /\. {
        deny all;
    }

    # Logs
    access_log /var/log/nginx/amcd57-access.log;
    error_log /var/log/nginx/amcd57-error.log;
}

# Configuration HTTPS (à décommenter après installation SSL)
# server {
#     listen 443 ssl http2;
#     listen [::]:443 ssl http2;
#     server_name amcd.alodev.ovh www.amcd.alodev.ovh;
#
#     # Certificats SSL (seront générés par Certbot)
#     ssl_certificate /etc/letsencrypt/live/amcd.alodev.ovh/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/amcd.alodev.ovh/privkey.pem;
#     include /etc/letsencrypt/options-ssl-nginx.conf;
#     ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
#
#     # Configuration SSL moderne
#     ssl_protocols TLSv1.2 TLSv1.3;
#     ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
#     ssl_prefer_server_ciphers off;
#
#     # HSTS (décommenter après test SSL)
#     # add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
#
#     # Headers de sécurité
#     add_header X-Frame-Options "SAMEORIGIN" always;
#     add_header X-Content-Type-Options "nosniff" always;
#     add_header X-XSS-Protection "1; mode=block" always;
#     add_header Referrer-Policy "no-referrer-when-downgrade" always;
#
#     # Taille maximale upload
#     client_max_body_size 20M;
#
#     location / {
#         proxy_pass http://amcd57_app;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_redirect off;
#     }
#
#     location /static/ {
#         alias /var/www/amcd57/staticfiles/;
#         expires 30d;
#         add_header Cache-Control "public, immutable";
#     }
#
#     location /media/ {
#         alias /var/www/amcd57/mediafiles/;
#         expires 30d;
#         add_header Cache-Control "public";
#     }
#
#     # Sécurité
#     location ~ /\. {
#         deny all;
#     }
#
#     # Logs
#     access_log /var/log/nginx/amcd57-ssl-access.log;
#     error_log /var/log/nginx/amcd57-ssl-error.log;
# }
```

### 2. Activer le site

```bash
# Créer le lien symbolique
sudo ln -s /etc/nginx/sites-available/amcd57 /etc/nginx/sites-enabled/

# ⚠️ IMPORTANT : Supprimer le site par défaut de Nginx
sudo rm /etc/nginx/sites-enabled/default

# Tester la configuration Nginx
sudo nginx -t

# Si OK, recharger Nginx
sudo systemctl reload nginx
```

**⚠️ IMPORTANT** : La suppression du site par défaut (`default`) est **essentielle**. Si vous ne le faites pas, Nginx servira la page "Welcome to nginx!" au lieu de votre site Django.

### 3. Vérifier le fonctionnement

```bash
# Tester depuis le VPS lui-même
curl http://localhost
# Vous devriez voir le HTML de votre site Django

# Tester avec le domaine
curl http://amcd.alodev.ovh

# Ouvrir dans le navigateur :
# http://amcd.alodev.ovh

# Le site devrait s'afficher !
```

**⚠️ DÉPANNAGE** : Si le site ne s'affiche pas :

```bash
# Vérifier que Nginx tourne
sudo systemctl status nginx

# Vérifier que Gunicorn tourne
sudo systemctl status gunicorn-amcd57

# Voir les logs Nginx
sudo tail -f /var/log/nginx/amcd57-error.log

# Voir les logs Gunicorn
sudo tail -f /var/www/amcd57/logs/gunicorn-error.log

# Vérifier que le port 80 est ouvert dans le firewall
sudo ufw status
# Si le port 80 n'est pas ouvert :
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## 🔒 Configuration SSL avec Certbot

### 1. Installer Certbot

```bash
# Installer Certbot pour Nginx
sudo apt install -y certbot python3-certbot-nginx
```

### 2. Obtenir le certificat SSL

```bash
# Obtenir le certificat pour le domaine temporaire
sudo certbot --nginx -d amcd.alodev.ovh -d www.amcd.alodev.ovh

# Suivre les instructions :
# - Entrer votre email (pour les notifications d'expiration)
# - Accepter les conditions
# - Choisir de rediriger automatiquement HTTP vers HTTPS (option 2)
```

### 3. Tester le renouvellement automatique

```bash
# Dry-run pour tester le renouvellement
sudo certbot renew --dry-run

# Si succès, le renouvellement automatique est configuré
```

### 4. Vérifier le certificat

```bash
# Vérifier l'expiration du certificat
sudo certbot certificates

# Tester HTTPS dans le navigateur :
# https://amcd.alodev.ovh
```

### 5. ⚠️ IMPORTANT : Réactiver les paramètres de sécurité HTTPS

**Une fois le certificat SSL installé**, il faut réactiver les paramètres de sécurité dans le fichier `.env` :

```bash
# Éditer le fichier .env
nano /var/www/amcd57/.env

# Modifier les paramètres de sécurité (passer de False à True) :
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Sauvegarder et quitter (Ctrl+O, Entrée, Ctrl+X)

# Redémarrer Gunicorn pour prendre en compte les changements
sudo systemctl restart gunicorn-amcd57
```

**Note** : Certbot aura automatiquement modifié la configuration Nginx pour rediriger HTTP vers HTTPS. Chrome mettra en cache le HSTS - si vous aviez activé HSTS avant SSL, videz le cache HSTS Chrome : `chrome://net-internals/#hsts`

### 6. Renouvellement automatique

Certbot configure automatiquement un cron job ou un timer systemd pour renouveler les certificats. Vérifier :

```bash
# Vérifier le timer systemd
sudo systemctl list-timers | grep certbot

# Ou vérifier le cron
sudo cat /etc/cron.d/certbot
```

---

## 📁 Configuration des fichiers statiques et médias

### 1. Créer les répertoires

```bash
cd /var/www/amcd57

# Les répertoires sont créés par collectstatic
# Vérifier qu'ils existent
ls -la staticfiles/
ls -la mediafiles/
```

### 2. Configurer les permissions

```bash
# Donner les bonnes permissions
sudo chown -R amcd:www-data /var/www/amcd57/staticfiles
sudo chown -R amcd:www-data /var/www/amcd57/media

sudo chmod -R 755 /var/www/amcd57/staticfiles
sudo chmod -R 755 /var/www/amcd57/media
```

### 3. Collecter les fichiers statiques

```bash
cd /var/www/amcd57
source venv/bin/activate

# Collecter les statiques
python manage.py collectstatic --noinput

# Redémarrer Gunicorn
sudo systemctl restart gunicorn-amcd57
```

---

## 📦 Migration des données depuis le développement

Si vous avez des données (articles, événements, etc.) dans votre environnement de développement local et que vous souhaitez les migrer vers la production :

### 1. Sur votre machine locale : Exporter les données

```bash
# Activer l'environnement virtuel local
source venv/bin/activate

# Exporter toutes les données sauf les utilisateurs et profils
python manage.py dumpdata \
  --exclude contenttypes \
  --exclude auth.Permission \
  --exclude sessions \
  --exclude auth.User \
  --exclude members.ProfilMembre \
  --exclude account.emailaddress \
  --exclude admin.logentry \
  --indent 2 > data_export.json

# Vérifier le fichier
ls -lh data_export.json
```

### 2. Réassigner les références utilisateur

Les articles et événements ont des références à des utilisateurs (auteur, organisateur) qui n'existent pas en production. Utilisez le script de migration :

```bash
# Le script migrate_data.py est dans le dépôt Git (scripts/migrate_data.py)
# Il réassigne tous les contenus à l'utilisateur ID=1 (le superutilisateur en production)

python scripts/migrate_data.py data_export.json data_production.json 1

# Cela crée data_production.json avec toutes les références utilisateur pointant vers l'utilisateur ID=1
```

### 3. Transférer les données vers le VPS

```bash
# Transférer le fichier JSON
scp data_production.json amcd@<IP_VPS>:/var/www/amcd57/

# Si vous avez des images/médias dans votre dossier media/ local
scp -r media/* amcd@<IP_VPS>:/var/www/amcd57/media/
```

### 4. Sur le VPS : Importer les données

```bash
# Se connecter au VPS
ssh amcd@<IP_VPS>

# Aller dans le répertoire du projet
cd /var/www/amcd57
source venv/bin/activate

# Importer les données
python manage.py loaddata data_production.json

# Si vous avez transféré des médias, corriger les permissions
sudo chown -R amcd:amcd media/
sudo chmod -R 755 media/

# Redémarrer Gunicorn
sudo systemctl restart gunicorn-amcd57
```

### 5. Vérifier l'import

```bash
# Vérifier dans l'admin Django
# https://amcd.alodev.ovh/admin/

# Ou lister les objets en shell
python manage.py shell
>>> from blog.models import Article
>>> Article.objects.count()
>>> exit()
```

**⚠️ IMPORTANT** : Cette méthode crée les données en production. Si vous avez déjà des données en production et que vous voulez les écraser, videz d'abord la base avec `python manage.py flush` (⚠️ destructif !).

---

## ⚙️ Variables d'environnement de production

### Fichier .env complet pour production

Créer/éditer `/var/www/amcd57/.env` :

```env
# ========================================
# Django Core Configuration
# ========================================
SECRET_KEY=votre_cle_secrete_generee_avec_django
DEBUG=False
ALLOWED_HOSTS=amcd.alodev.ovh,www.amcd.alodev.ovh,<IP_VPS>

# ========================================
# Database Configuration
# ========================================
DB_NAME=amcd57_db
DB_USER=amcd57_user
DB_PASSWORD=votre_mot_de_passe_postgresql
DB_HOST=localhost
DB_PORT=5432

# ========================================
# Email Configuration (Gmail exemple)
# ========================================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre.email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_application_gmail
DEFAULT_FROM_EMAIL=AMCD57 <votre.email@gmail.com>
SERVER_EMAIL=votre.email@gmail.com

# ========================================
# APIs
# ========================================
OPENWEATHER_API_KEY=votre_cle_api_openweathermap

# ========================================
# Security Settings
# ========================================
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# ========================================
# Site Configuration
# ========================================
SITE_ID=1
```

### Sécuriser le fichier .env

```bash
# Permissions strictes
chmod 600 /var/www/amcd57/.env

# Vérifier que seul amcd peut le lire
ls -la /var/www/amcd57/.env
```

---

## 💾 Mise en place des sauvegardes

### 1. Script de sauvegarde de la base de données

```bash
# Créer le répertoire pour les sauvegardes
sudo mkdir -p /var/backups/amcd57
sudo chown amcd:amcd /var/backups/amcd57

# Créer le script de backup
vim /home/amcd/backup_amcd57.sh
```

Contenu de `backup_amcd57.sh` :

```bash
#!/bin/bash

# Script de sauvegarde AMCD57
# Sauvegarde la base de données PostgreSQL et les fichiers média

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/amcd57"
DB_NAME="amcd57_db"
DB_USER="amcd57_user"
APP_DIR="/var/www/amcd57"

# Créer le répertoire du jour
mkdir -p "$BACKUP_DIR/$DATE"

# Backup de la base de données
echo "Backup de la base de données..."
PGPASSWORD="VOTRE_MOT_DE_PASSE" pg_dump -U $DB_USER -h localhost $DB_NAME > "$BACKUP_DIR/$DATE/database.sql"
gzip "$BACKUP_DIR/$DATE/database.sql"

# Backup des fichiers média
echo "Backup des fichiers média..."
tar -czf "$BACKUP_DIR/$DATE/mediafiles.tar.gz" -C "$APP_DIR" mediafiles/

# Backup du fichier .env
echo "Backup de la configuration..."
cp "$APP_DIR/.env" "$BACKUP_DIR/$DATE/.env"

# Nettoyer les backups de plus de 30 jours
echo "Nettoyage des anciens backups..."
find "$BACKUP_DIR" -type d -mtime +30 -exec rm -rf {} +

echo "Backup terminé : $BACKUP_DIR/$DATE"
```

Rendre le script exécutable :

```bash
chmod +x /home/amcd/backup_amcd57.sh
```

### 2. Configurer le cron pour sauvegardes automatiques

```bash
# Éditer la crontab
crontab -e

# Ajouter cette ligne (backup tous les jours à 3h du matin)
0 3 * * * /home/amcd/backup_amcd57.sh >> /var/log/backup_amcd57.log 2>&1
```

### 3. Tester le script de backup

```bash
# Exécuter manuellement
/home/amcd/backup_amcd57.sh

# Vérifier que les fichiers sont créés
ls -lh /var/backups/amcd57/
```

### 4. Script de restauration

Créer `/home/amcd/restore_amcd57.sh` :

```bash
#!/bin/bash

# Script de restauration AMCD57
# Usage: ./restore_amcd57.sh YYYYMMDD_HHMMSS

if [ -z "$1" ]; then
    echo "Usage: $0 YYYYMMDD_HHMMSS"
    echo "Exemple: $0 20250125_030000"
    exit 1
fi

BACKUP_DATE=$1
BACKUP_DIR="/var/backups/amcd57/$BACKUP_DATE"
DB_NAME="amcd57_db"
DB_USER="amcd57_user"
APP_DIR="/var/www/amcd57"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup non trouvé : $BACKUP_DIR"
    exit 1
fi

echo "Restauration depuis : $BACKUP_DIR"
read -p "Êtes-vous sûr ? (yes/no) " -n 3 -r
echo
if [[ ! $REPLY =~ ^yes$ ]]; then
    exit 1
fi

# Arrêter Gunicorn
echo "Arrêt de Gunicorn..."
sudo systemctl stop gunicorn-amcd57

# Restaurer la base de données
echo "Restauration de la base de données..."
gunzip -c "$BACKUP_DIR/database.sql.gz" | PGPASSWORD="VOTRE_MOT_DE_PASSE" psql -U $DB_USER -h localhost $DB_NAME

# Restaurer les fichiers média
echo "Restauration des fichiers média..."
rm -rf "$APP_DIR/mediafiles"
tar -xzf "$BACKUP_DIR/mediafiles.tar.gz" -C "$APP_DIR"

# Redémarrer Gunicorn
echo "Redémarrage de Gunicorn..."
sudo systemctl start gunicorn-amcd57

echo "Restauration terminée !"
```

Rendre exécutable :

```bash
chmod +x /home/amcd/restore_amcd57.sh
```

---

## 📊 Monitoring et logs

### 1. Configurer logrotate pour les logs Django

```bash
sudo vim /etc/logrotate.d/amcd57
```

Contenu :

```
/var/www/amcd57/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 amcd www-data
    sharedscripts
    postrotate
        systemctl reload gunicorn-amcd57 > /dev/null
    endscript
}
```

### 2. Commandes utiles pour les logs

```bash
# Logs Gunicorn en temps réel
sudo journalctl -u gunicorn-amcd57 -f

# Logs Nginx access
sudo tail -f /var/log/nginx/amcd57-access.log

# Logs Nginx error
sudo tail -f /var/log/nginx/amcd57-error.log

# Logs Django (si configurés)
tail -f /var/www/amcd57/logs/gunicorn-access.log
tail -f /var/www/amcd57/logs/gunicorn-error.log

# Logs PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-16-main.log
```

### 3. Monitoring simple avec htop

```bash
# Installer htop
sudo apt install -y htop

# Lancer htop
htop
```

### 4. Monitoring de l'espace disque

```bash
# Voir l'espace disque utilisé
df -h

# Voir la taille des répertoires
du -sh /var/www/amcd57/*
du -sh /var/backups/amcd57/*
```

---

## 🔄 Migration vers le domaine définitif

### Quand vous serez prêt à passer sur www.amcd57.fr

### 1. Configuration DNS pour www.amcd57.fr

Configurer les enregistrements DNS :

```
Type    Sous-domaine    Cible           TTL
A       @               <IP_VPS>        3600
A       www             <IP_VPS>        3600
```

### 2. Modifier la configuration Nginx

```bash
# Éditer la configuration
sudo vim /etc/nginx/sites-available/amcd57

# Remplacer toutes les occurrences de :
# amcd.alodev.ovh par www.amcd57.fr

# Tester
sudo nginx -t

# Recharger
sudo systemctl reload nginx
```

### 3. Obtenir un nouveau certificat SSL

```bash
# Obtenir le certificat pour le nouveau domaine
sudo certbot --nginx -d www.amcd57.fr -d amcd57.fr

# Certbot va automatiquement modifier la configuration Nginx
```

### 4. Mettre à jour le fichier .env

```bash
vim /var/www/amcd57/.env

# Modifier ALLOWED_HOSTS
ALLOWED_HOSTS=www.amcd57.fr,amcd57.fr,<IP_VPS>
```

### 5. Redémarrer les services

```bash
sudo systemctl restart gunicorn-amcd57
sudo systemctl reload nginx
```

### 6. Configurer une redirection depuis l'ancien domaine (optionnel)

Ajouter dans la configuration Nginx :

```nginx
# Redirection depuis l'ancien domaine
server {
    listen 80;
    listen 443 ssl http2;
    server_name amcd.alodev.ovh www.amcd.alodev.ovh;

    # Certificat SSL (existant)
    ssl_certificate /etc/letsencrypt/live/amcd.alodev.ovh/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/amcd.alodev.ovh/privkey.pem;

    return 301 https://www.amcd57.fr$request_uri;
}
```

---

## ✅ Checklist finale

### Avant le déploiement

- [ ] Code testé localement (`python manage.py test`)
- [ ] Check de déploiement passé (`python manage.py check --deploy`)
- [ ] Code poussé sur GitHub
- [ ] DNS configuré et propagé
- [ ] VPS accessible via SSH
- [ ] Utilisateur non-root créé avec sudo

### Après le déploiement

#### Sécurité
- [ ] Pare-feu UFW activé et configuré
- [ ] SSH sécurisé (root désactivé, authentification par clé)
- [ ] SSL/HTTPS activé avec Certbot
- [ ] Headers de sécurité configurés dans Nginx
- [ ] DEBUG=False dans .env
- [ ] SECRET_KEY unique et sécurisée
- [ ] Fichier .env protégé (chmod 600)

#### Services
- [ ] PostgreSQL installé et base créée
- [ ] Migrations Django effectuées
- [ ] Superutilisateur créé
- [ ] Gunicorn configuré et démarré
- [ ] Nginx configuré et démarré
- [ ] Fichiers statiques collectés
- [ ] Certificat SSL obtenu et valide

#### Fonctionnalités
- [ ] Site accessible en HTTPS
- [ ] Pages principales fonctionnelles
- [ ] Interface admin accessible
- [ ] Upload d'images fonctionne
- [ ] Emails configurés et testés
- [ ] Widget météo fonctionne

#### Monitoring & Maintenance
- [ ] Sauvegardes automatiques configurées
- [ ] Script de restauration testé
- [ ] Logs rotatifs configurés
- [ ] Renouvellement SSL automatique vérifié
- [ ] Monitoring basique en place

#### Tests finaux
- [ ] Tester l'inscription à un événement
- [ ] Tester la création d'un article
- [ ] Tester l'upload d'une image
- [ ] Tester le formulaire de contact
- [ ] Tester l'admin Django
- [ ] Tester sur mobile

---

## 🆘 Dépannage

### Problème : Gunicorn ne démarre pas

```bash
# Voir les erreurs
sudo journalctl -u gunicorn-amcd57 -n 50

# Vérifier les permissions
ls -la /var/www/amcd57

# Tester manuellement
cd /var/www/amcd57
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 amcd57_project.wsgi:application
```

### Problème : Erreur 502 Bad Gateway

```bash
# Vérifier que Gunicorn tourne
sudo systemctl status gunicorn-amcd57

# Vérifier les logs Nginx
sudo tail -f /var/log/nginx/amcd57-error.log

# Redémarrer les services
sudo systemctl restart gunicorn-amcd57
sudo systemctl reload nginx
```

### Problème : Les fichiers statiques ne se chargent pas

```bash
# Recollect des statiques
cd /var/www/amcd57
source venv/bin/activate
python manage.py collectstatic --noinput

# Vérifier les permissions
sudo chown -R amcd:www-data /var/www/amcd57/staticfiles
sudo chmod -R 755 /var/www/amcd57/staticfiles

# Vérifier la config Nginx
sudo nginx -t
sudo systemctl reload nginx
```

### Problème : Erreurs de connexion à la base de données

```bash
# Vérifier que PostgreSQL tourne
sudo systemctl status postgresql

# Tester la connexion
psql -U amcd57_user -d amcd57_db -h localhost

# Vérifier le fichier .env
cat /var/www/amcd57/.env | grep DB_

# Redémarrer PostgreSQL
sudo systemctl restart postgresql
```

### Problème : SSL ne fonctionne pas

```bash
# Vérifier les certificats
sudo certbot certificates

# Tester la configuration Nginx
sudo nginx -t

# Renouveler manuellement
sudo certbot renew

# Vérifier les logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

---

## 📚 Ressources utiles

- [Documentation Django Deployment](https://docs.djangoproject.com/en/5.0/howto/deployment/)
- [Documentation Gunicorn](https://docs.gunicorn.org/)
- [Documentation Nginx](https://nginx.org/en/docs/)
- [Documentation Certbot](https://certbot.eff.org/)
- [Django Security Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)

---

## 🎉 Félicitations !

Si vous êtes arrivé jusqu'ici et que tout fonctionne, votre site AMCD57 est maintenant déployé en production sur votre VPS OVH !

N'oubliez pas de :
- Surveiller régulièrement les logs
- Vérifier que les sauvegardes fonctionnent
- Mettre à jour régulièrement Django et les dépendances
- Tester les fonctionnalités après chaque mise à jour

Bon vol ! ✈️
