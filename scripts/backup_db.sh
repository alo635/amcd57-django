#!/bin/bash
#
# Script de backup automatique de la base de données PostgreSQL
# AMCD57 - Base de données de production
#
# Usage: ./backup_db.sh
# Cron: 0 2 * * * /var/www/amcd57/scripts/backup_db.sh

set -e

# Configuration
BACKUP_DIR="/var/www/amcd57/backups/db"
DB_NAME="amcd57_db"
DB_USER="amcd57_user"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/amcd57_db_${TIMESTAMP}.sql.gz"
RETENTION_DAYS=30

# Créer le répertoire de backup s'il n'existe pas
mkdir -p "${BACKUP_DIR}"

# Backup de la base de données (compressé)
echo "🔄 Début du backup de la base de données..."
pg_dump -U "${DB_USER}" -h localhost "${DB_NAME}" | gzip > "${BACKUP_FILE}"

# Vérifier que le backup a réussi
if [ $? -eq 0 ]; then
    echo "✅ Backup réussi : ${BACKUP_FILE}"

    # Afficher la taille du backup
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "📦 Taille du backup : ${SIZE}"
else
    echo "❌ Erreur lors du backup"
    exit 1
fi

# Nettoyer les anciens backups (conservation de ${RETENTION_DAYS} jours)
echo "🧹 Nettoyage des backups de plus de ${RETENTION_DAYS} jours..."
find "${BACKUP_DIR}" -name "amcd57_db_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete

# Lister les backups restants
echo "📋 Backups disponibles :"
ls -lh "${BACKUP_DIR}" | grep "amcd57_db_" | tail -n 5

echo "✅ Backup terminé avec succès"
