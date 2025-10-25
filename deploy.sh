#!/bin/bash

# ========================================
# Script de déploiement rapide AMCD57
# ========================================
# Usage: ./deploy.sh
# À exécuter sur le serveur dans /var/www/amcd57

set -e  # Arrêter en cas d'erreur

echo "🚀 Déploiement AMCD57 en cours..."

# Vérifier qu'on est dans le bon répertoire
if [ ! -f "manage.py" ]; then
    echo "❌ Erreur : ce script doit être exécuté depuis /var/www/amcd57"
    exit 1
fi

# 1. Pull du dernier code
echo "📥 1. Récupération du dernier code..."
git pull origin main

# 2. Activer l'environnement virtuel
echo "🐍 2. Activation de l'environnement virtuel..."
source venv/bin/activate

# 3. Installer/mettre à jour les dépendances
echo "📦 3. Installation des dépendances..."
pip install -r requirements.txt --upgrade

# 4. Collecter les fichiers statiques
echo "📁 4. Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# 5. Effectuer les migrations
echo "🗄️  5. Migrations de la base de données..."
python manage.py migrate --noinput

# 6. Redémarrer Gunicorn
echo "🔄 6. Redémarrage de Gunicorn..."
sudo systemctl restart gunicorn-amcd57

# 7. Recharger Nginx
echo "🌐 7. Rechargement de Nginx..."
sudo systemctl reload nginx

# 8. Vérifier le statut
echo ""
echo "✅ Déploiement terminé !"
echo ""
echo "📊 Statut des services :"
sudo systemctl status gunicorn-amcd57 --no-pager -l | head -n 5
echo ""
sudo systemctl status nginx --no-pager -l | head -n 5

echo ""
echo "🎉 Le site est à jour sur https://amcd.alodev.ovh"
echo ""
echo "📝 Pour voir les logs en temps réel :"
echo "   sudo journalctl -u gunicorn-amcd57 -f"
