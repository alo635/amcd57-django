#!/bin/bash
#
# Script de restauration de la base de données PostgreSQL
# AMCD57 - Restauration depuis un backup
#
# Usage: ./restore_db.sh <fichier_backup.sql.gz>
# Exemple: ./restore_db.sh /var/www/amcd57/backups/db/amcd57_db_20251026_120000.sql.gz

set -e

# Configuration
DB_NAME="amcd57_db"
DB_USER="amcd57_user"
BACKUP_FILE="$1"

# Vérifier qu'un fichier a été fourni
if [ -z "${BACKUP_FILE}" ]; then
    echo "❌ Erreur : Veuillez spécifier un fichier de backup"
    echo "Usage: $0 <fichier_backup.sql.gz>"
    echo ""
    echo "📋 Backups disponibles :"
    ls -lh /var/www/amcd57/backups/db/ | grep "amcd57_db_"
    exit 1
fi

# Vérifier que le fichier existe
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "❌ Erreur : Le fichier ${BACKUP_FILE} n'existe pas"
    exit 1
fi

# Confirmation avant restauration
echo "⚠️  ATTENTION : Vous allez restaurer la base de données depuis :"
echo "   ${BACKUP_FILE}"
echo ""
echo "   Cela va ÉCRASER toutes les données actuelles de la base ${DB_NAME}"
echo ""
read -p "   Êtes-vous sûr de vouloir continuer ? (oui/non) : " CONFIRMATION

if [ "${CONFIRMATION}" != "oui" ]; then
    echo "❌ Restauration annulée"
    exit 0
fi

# Backup de sécurité avant restauration
SAFETY_BACKUP="/var/www/amcd57/backups/db/before_restore_$(date +%Y%m%d_%H%M%S).sql.gz"
echo "🔄 Création d'un backup de sécurité avant restauration..."
pg_dump -U "${DB_USER}" -h localhost "${DB_NAME}" | gzip > "${SAFETY_BACKUP}"
echo "✅ Backup de sécurité créé : ${SAFETY_BACKUP}"

# Arrêter Gunicorn pour éviter les connexions actives
echo "🛑 Arrêt de Gunicorn..."
sudo systemctl stop gunicorn-amcd57

# Supprimer la base de données existante
echo "🗑️  Suppression de la base de données actuelle..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS ${DB_NAME};"

# Recréer la base de données
echo "🔨 Recréation de la base de données..."
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

# Restaurer depuis le backup
echo "📥 Restauration des données depuis le backup..."
gunzip -c "${BACKUP_FILE}" | psql -U "${DB_USER}" -h localhost -d "${DB_NAME}"

if [ $? -eq 0 ]; then
    echo "✅ Restauration réussie"
else
    echo "❌ Erreur lors de la restauration"
    echo "⚠️  Vous pouvez restaurer le backup de sécurité avec :"
    echo "   gunzip -c ${SAFETY_BACKUP} | psql -U ${DB_USER} -h localhost -d ${DB_NAME}"
    exit 1
fi

# Redémarrer Gunicorn
echo "🚀 Redémarrage de Gunicorn..."
sudo systemctl start gunicorn-amcd57

echo "✅ Restauration terminée avec succès"
echo "📦 Backup de sécurité conservé : ${SAFETY_BACKUP}"
