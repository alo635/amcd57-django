#!/bin/bash
#
# Script de backup des fichiers média
# AMCD57 - Sauvegarde des uploads utilisateurs
#
# Usage: ./backup_media.sh
# Cron: 0 3 * * * /var/www/amcd57/scripts/backup_media.sh

set -e

# Configuration
BACKUP_DIR="/var/www/amcd57/backups/media"
MEDIA_DIR="/var/www/amcd57/media"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/media_${TIMESTAMP}.tar.gz"
RETENTION_DAYS=60

# Créer le répertoire de backup s'il n'existe pas
mkdir -p "${BACKUP_DIR}"

# Vérifier que le répertoire media existe
if [ ! -d "${MEDIA_DIR}" ]; then
    echo "❌ Erreur : Le répertoire ${MEDIA_DIR} n'existe pas"
    exit 1
fi

# Backup des fichiers média (compressé)
echo "🔄 Début du backup des fichiers média..."
tar -czf "${BACKUP_FILE}" -C "$(dirname ${MEDIA_DIR})" "$(basename ${MEDIA_DIR})"

# Vérifier que le backup a réussi
if [ $? -eq 0 ]; then
    echo "✅ Backup réussi : ${BACKUP_FILE}"

    # Afficher la taille du backup
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "📦 Taille du backup : ${SIZE}"

    # Compter le nombre de fichiers
    COUNT=$(tar -tzf "${BACKUP_FILE}" | wc -l)
    echo "📁 Nombre de fichiers sauvegardés : ${COUNT}"
else
    echo "❌ Erreur lors du backup"
    exit 1
fi

# Nettoyer les anciens backups (conservation de ${RETENTION_DAYS} jours)
echo "🧹 Nettoyage des backups de plus de ${RETENTION_DAYS} jours..."
find "${BACKUP_DIR}" -name "media_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete

# Lister les backups restants
echo "📋 Backups disponibles :"
ls -lh "${BACKUP_DIR}" | grep "media_" | tail -n 5

echo "✅ Backup terminé avec succès"
