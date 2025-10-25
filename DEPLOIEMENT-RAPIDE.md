# 🚀 Déploiement Rapide - Aide-mémoire

Guide condensé pour déployer rapidement AMCD57 sur VPS OVH.

> 📖 **Guide complet** : Voir [DEPLOIEMENT.md](DEPLOIEMENT.md)

---

## 🎯 Prérequis

- VPS OVH Ubuntu 25.04
- Domaine : `amcd.alodev.ovh` configuré (DNS pointant vers IP du VPS)
- Accès SSH root au VPS
- Email pour SSL
- Clé API OpenWeatherMap

---

## ⚡ Installation Express (30 minutes)

### 1️⃣ Connexion et sécurisation (5 min)

```bash
# Se connecter au VPS
ssh root@<IP_VPS>

# Mise à jour système
apt update && apt upgrade -y

# Installer utilitaires de base
apt install -y curl wget git vim ufw build-essential software-properties-common

# Créer utilisateur non-root
adduser amcd
usermod -aG sudo amcd

# Configurer pare-feu
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable

# Se reconnecter avec le nouvel utilisateur
exit
ssh amcd@<IP_VPS>
```

### 2️⃣ Installation des dépendances (10 min)

```bash
# Python 3.13
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.13 python3.13-venv python3.13-dev

# PostgreSQL
sudo apt install -y postgresql postgresql-contrib libpq-dev

# Nginx
sudo apt install -y nginx

# Dépendances Pillow
sudo apt install -y libjpeg-dev zlib1g-dev libpng-dev
```

### 3️⃣ Configuration PostgreSQL (3 min)

```bash
sudo -u postgres psql

# Dans PostgreSQL :
CREATE DATABASE amcd57_db;
CREATE USER amcd57_user WITH PASSWORD 'VOTRE_MOT_DE_PASSE';
ALTER ROLE amcd57_user SET client_encoding TO 'utf8';
ALTER ROLE amcd57_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE amcd57_user SET timezone TO 'Europe/Paris';
GRANT ALL PRIVILEGES ON DATABASE amcd57_db TO amcd57_user;
\q
```

### 4️⃣ Déploiement Django (7 min)

```bash
# Créer répertoire
sudo mkdir -p /var/www/amcd57
sudo chown -R amcd:amcd /var/www/amcd57
cd /var/www/amcd57

# Cloner le projet
git clone https://github.com/alo635/amcd57-django.git .

# Environnement virtuel
python3.13 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install --upgrade pip
pip install -r requirements-prod.txt

# Créer .env (IMPORTANT : modifier avec vos vraies valeurs !)
cp .env.production.example .env
vim .env  # Modifier SECRET_KEY, mots de passe, etc.

# Django setup
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser

# Créer répertoire logs
mkdir -p logs
```

### 5️⃣ Configuration Gunicorn (2 min)

```bash
# Le fichier gunicorn_config.py est déjà dans le repo

# Créer le service systemd
sudo vim /etc/systemd/system/gunicorn-amcd57.service
```

Copier le contenu depuis [DEPLOIEMENT.md section Gunicorn](DEPLOIEMENT.md#configuration-gunicorn)

```bash
# Activer et démarrer
sudo systemctl daemon-reload
sudo systemctl enable gunicorn-amcd57
sudo systemctl start gunicorn-amcd57
sudo systemctl status gunicorn-amcd57
```

### 6️⃣ Configuration Nginx (2 min)

```bash
# Créer la configuration
sudo vim /etc/nginx/sites-available/amcd57
```

Copier le contenu depuis [DEPLOIEMENT.md section Nginx](DEPLOIEMENT.md#configuration-nginx)

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/amcd57 /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Tester et recharger
sudo nginx -t
sudo systemctl reload nginx
```

**✅ Le site devrait maintenant être accessible en HTTP : `http://amcd.alodev.ovh`**

### 7️⃣ Installer SSL (1 min)

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir le certificat (suivre les instructions)
sudo certbot --nginx -d amcd.alodev.ovh -d www.amcd.alodev.ovh
```

**🎉 Le site est maintenant en HTTPS : `https://amcd.alodev.ovh`**

---

## 🔄 Mises à jour futures

Après chaque modification du code :

```bash
# Sur le serveur
cd /var/www/amcd57
chmod +x deploy.sh
./deploy.sh
```

---

## 📊 Commandes utiles

```bash
# Logs en temps réel
sudo journalctl -u gunicorn-amcd57 -f

# Redémarrer les services
sudo systemctl restart gunicorn-amcd57
sudo systemctl reload nginx

# Vérifier le statut
sudo systemctl status gunicorn-amcd57
sudo systemctl status nginx
sudo systemctl status postgresql

# Espace disque
df -h
du -sh /var/www/amcd57/*
```

---

## 🆘 Dépannage rapide

**Erreur 502 Bad Gateway**
```bash
sudo systemctl restart gunicorn-amcd57
sudo systemctl reload nginx
sudo journalctl -u gunicorn-amcd57 -n 50
```

**Base de données inaccessible**
```bash
sudo systemctl status postgresql
psql -U amcd57_user -d amcd57_db -h localhost
```

**Fichiers statiques ne chargent pas**
```bash
cd /var/www/amcd57
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-amcd57
```

---

## 📝 Checklist finale

- [ ] Site accessible en HTTPS
- [ ] Admin Django fonctionne (`/admin/`)
- [ ] Création d'article fonctionne
- [ ] Upload d'image fonctionne
- [ ] Formulaire de contact fonctionne
- [ ] Widget météo s'affiche
- [ ] Inscription événement fonctionne
- [ ] Certificat SSL valide (cadenas vert)
- [ ] Redirection HTTP → HTTPS active

---

## 🔐 Sécurité post-déploiement

```bash
# Sécuriser le fichier .env
chmod 600 /var/www/amcd57/.env

# Désactiver le login root SSH
sudo vim /etc/ssh/sshd_config
# PermitRootLogin no
sudo systemctl restart sshd

# Configurer les backups (voir DEPLOIEMENT.md section Sauvegardes)
```

---

## 📚 Pour aller plus loin

- Sauvegardes automatiques → [DEPLOIEMENT.md](DEPLOIEMENT.md#mise-en-place-des-sauvegardes)
- Monitoring et logs → [DEPLOIEMENT.md](DEPLOIEMENT.md#monitoring-et-logs)
- Migration vers domaine définitif → [DEPLOIEMENT.md](DEPLOIEMENT.md#migration-vers-le-domaine-définitif)

---

**✈️ Bon vol avec AMCD57 !**
