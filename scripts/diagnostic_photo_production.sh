#!/bin/bash
# Script de diagnostic pour le problème d'upload de photo en production

echo "=========================================="
echo "DIAGNOSTIC UPLOAD PHOTO AMCD57 PRODUCTION"
echo "=========================================="
echo ""

echo "1️⃣  VÉRIFICATION DU RÉPERTOIRE MEDIA"
echo "-----------------------------------"
if [ -d "/var/www/amcd57/media" ]; then
    echo "✅ Répertoire media existe"
    ls -la /var/www/amcd57/media/
else
    echo "❌ Répertoire media n'existe pas !"
fi
echo ""

echo "2️⃣  VÉRIFICATION DU RÉPERTOIRE MEMBERS/PHOTOS"
echo "-------------------------------------------"
if [ -d "/var/www/amcd57/media/members/photos" ]; then
    echo "✅ Répertoire members/photos existe"
    ls -la /var/www/amcd57/media/members/photos/
else
    echo "⚠️  Répertoire members/photos n'existe pas"
    echo "Création du répertoire..."
    mkdir -p /var/www/amcd57/media/members/photos/
    echo "✅ Répertoire créé"
fi
echo ""

echo "3️⃣  PERMISSIONS DU RÉPERTOIRE MEDIA"
echo "---------------------------------"
stat -c "%a %U:%G %n" /var/www/amcd57/media/ 2>/dev/null || stat -f "%Lp %Su:%Sg %N" /var/www/amcd57/media/
echo ""

echo "4️⃣  TEST D'ÉCRITURE DANS MEDIA"
echo "----------------------------"
TEST_FILE="/var/www/amcd57/media/members/photos/test_$(date +%s).txt"
if echo "test" > "$TEST_FILE" 2>/dev/null; then
    echo "✅ Écriture réussie dans media/members/photos/"
    rm "$TEST_FILE"
else
    echo "❌ IMPOSSIBLE D'ÉCRIRE dans media/members/photos/"
    echo "   → C'est probablement LE problème !"
fi
echo ""

echo "5️⃣  UTILISATEUR GUNICORN"
echo "----------------------"
echo "Service Gunicorn lancé par :"
ps aux | grep gunicorn | grep -v grep | awk '{print $1}' | head -1 || echo "❌ Gunicorn ne tourne pas"
echo ""

echo "6️⃣  CONFIGURATION NGINX MEDIA"
echo "----------------------------"
if grep -q "location /media/" /etc/nginx/sites-available/amcd57 2>/dev/null; then
    echo "✅ Configuration Nginx media trouvée :"
    grep -A 5 "location /media/" /etc/nginx/sites-available/amcd57
else
    echo "❌ Configuration Nginx media non trouvée"
fi
echo ""

echo "7️⃣  VARIABLES MEDIA DANS .ENV"
echo "----------------------------"
if [ -f "/var/www/amcd57/.env" ]; then
    grep MEDIA /var/www/amcd57/.env || echo "⚠️  Pas de variables MEDIA dans .env"
elif [ -f "/var/www/amcd57/.env.production" ]; then
    grep MEDIA /var/www/amcd57/.env.production || echo "⚠️  Pas de variables MEDIA dans .env.production"
else
    echo "❌ Fichier .env non trouvé"
fi
echo ""

echo "8️⃣  PILLOW INSTALLÉ ?"
echo "--------------------"
/var/www/amcd57/venv/bin/python -c "import PIL; print(f'✅ Pillow version: {PIL.__version__}')" 2>/dev/null || echo "❌ Pillow non installé"
echo ""

echo "9️⃣  LOGS GUNICORN (20 dernières lignes)"
echo "--------------------------------------"
if [ -f "/var/www/amcd57/logs/gunicorn-error.log" ]; then
    tail -n 20 /var/www/amcd57/logs/gunicorn-error.log
else
    echo "❌ Fichier de log Gunicorn non trouvé à /var/www/amcd57/logs/gunicorn-error.log"
    echo "Recherche d'autres emplacements..."
    find /var/www/amcd57 -name "*gunicorn*.log" 2>/dev/null || echo "Aucun log trouvé"
fi
echo ""

echo "🔟 LOGS SYSTEMD GUNICORN (20 dernières lignes)"
echo "---------------------------------------------"
sudo journalctl -u gunicorn-amcd57 -n 20 --no-pager 2>/dev/null || echo "❌ Service gunicorn-amcd57 non trouvé dans systemd"
echo ""

echo "=========================================="
echo "FIN DU DIAGNOSTIC"
echo "=========================================="
echo ""
echo "🔧 ACTIONS RECOMMANDÉES :"
echo ""
echo "Si le test d'écriture a échoué, exécutez :"
echo "  sudo chown -R amcd:amcd /var/www/amcd57/media/"
echo "  sudo chmod -R 775 /var/www/amcd57/media/"
echo ""
echo "Pour suivre les logs en temps réel pendant un test d'upload :"
echo "  sudo journalctl -u gunicorn-amcd57 -f"
echo ""
