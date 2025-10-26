#!/bin/bash
#
# Script d'installation et configuration des backups automatiques
# AMCD57 - Configuration initiale
#
# Usage: sudo ./setup_backups.sh

set -e

echo "🔧 Configuration des backups automatiques AMCD57"
echo "================================================"
echo ""

# Vérifier que le script est exécuté en root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Erreur : Ce script doit être exécuté avec sudo"
    exit 1
fi

# Configuration
SCRIPTS_DIR="/var/www/amcd57/scripts"
BACKUP_DIR="/var/www/amcd57/backups"
USER="amcd"

echo "📁 Création des répertoires de backup..."
mkdir -p "${BACKUP_DIR}/db"
mkdir -p "${BACKUP_DIR}/media"
chown -R ${USER}:${USER} "${BACKUP_DIR}"
chmod -R 755 "${BACKUP_DIR}"

echo "🔑 Création du fichier .pgpass pour pg_dump sans mot de passe..."
PGPASS_FILE="/home/${USER}/.pgpass"

# Demander le mot de passe de la base de données
read -sp "Entrez le mot de passe PostgreSQL pour amcd57_user : " DB_PASSWORD
echo ""

# Créer le fichier .pgpass
echo "localhost:5432:amcd57_db:amcd57_user:${DB_PASSWORD}" > "${PGPASS_FILE}"
chown ${USER}:${USER} "${PGPASS_FILE}"
chmod 600 "${PGPASS_FILE}"

echo "✅ Fichier .pgpass créé"

echo "🔐 Rendre les scripts exécutables..."
chmod +x "${SCRIPTS_DIR}/backup_db.sh"
chmod +x "${SCRIPTS_DIR}/backup_media.sh"
chmod +x "${SCRIPTS_DIR}/restore_db.sh"

echo "⏰ Configuration des cron jobs..."

# Créer le fichier cron temporaire
CRON_FILE="/tmp/amcd_cron"

# Récupérer les crons existants de l'utilisateur
crontab -u ${USER} -l > "${CRON_FILE}" 2>/dev/null || true

# Vérifier si les crons existent déjà
if grep -q "backup_db.sh" "${CRON_FILE}"; then
    echo "⚠️  Les cron jobs existent déjà, mise à jour..."
    # Supprimer les anciens crons AMCD57
    grep -v "backup_db.sh\|backup_media.sh" "${CRON_FILE}" > "${CRON_FILE}.tmp" || true
    mv "${CRON_FILE}.tmp" "${CRON_FILE}"
fi

# Ajouter les nouveaux cron jobs
cat >> "${CRON_FILE}" << EOF

# AMCD57 - Backups automatiques
# Backup de la base de données tous les jours à 2h du matin
0 2 * * * ${SCRIPTS_DIR}/backup_db.sh >> /var/www/amcd57/logs/backup_db.log 2>&1

# Backup des fichiers média tous les jours à 3h du matin
0 3 * * * ${SCRIPTS_DIR}/backup_media.sh >> /var/www/amcd57/logs/backup_media.log 2>&1
EOF

# Installer les crons
crontab -u ${USER} "${CRON_FILE}"
rm "${CRON_FILE}"

echo "✅ Cron jobs configurés :"
echo "   - Backup DB    : Tous les jours à 2h00"
echo "   - Backup Media : Tous les jours à 3h00"
echo ""

# Test des scripts
echo "🧪 Test du script de backup de la base de données..."
sudo -u ${USER} ${SCRIPTS_DIR}/backup_db.sh

echo ""
echo "🧪 Test du script de backup des médias..."
sudo -u ${USER} ${SCRIPTS_DIR}/backup_media.sh

echo ""
echo "✅ Configuration terminée avec succès !"
echo ""
echo "📋 Informations importantes :"
echo "   - Répertoire des backups : ${BACKUP_DIR}"
echo "   - Logs des backups : /var/www/amcd57/logs/"
echo "   - Rétention DB : 30 jours"
echo "   - Rétention Media : 60 jours"
echo ""
echo "🔍 Commandes utiles :"
echo "   - Lister les backups DB : ls -lh ${BACKUP_DIR}/db/"
echo "   - Lister les backups Media : ls -lh ${BACKUP_DIR}/media/"
echo "   - Voir les logs backup DB : tail -f /var/www/amcd57/logs/backup_db.log"
echo "   - Voir les logs backup Media : tail -f /var/www/amcd57/logs/backup_media.log"
echo "   - Lister les cron jobs : crontab -u ${USER} -l"
echo "   - Restaurer la DB : ${SCRIPTS_DIR}/restore_db.sh <fichier_backup>"
echo ""
