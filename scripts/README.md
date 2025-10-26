# Scripts de Backup AMCD57

Ce répertoire contient les scripts de backup automatique pour le projet AMCD57.

## 📁 Scripts disponibles

### 1. `backup_db.sh`
Sauvegarde de la base de données PostgreSQL (compressée).

**Usage :**
```bash
./backup_db.sh
```

**Caractéristiques :**
- Compression gzip pour économiser l'espace
- Rétention de 30 jours
- Sauvegarde dans `/var/www/amcd57/backups/db/`
- Nommage : `amcd57_db_YYYYMMDD_HHMMSS.sql.gz`

### 2. `backup_media.sh`
Sauvegarde des fichiers média uploadés par les utilisateurs.

**Usage :**
```bash
./backup_media.sh
```

**Caractéristiques :**
- Archive tar.gz compressée
- Rétention de 60 jours
- Sauvegarde dans `/var/www/amcd57/backups/media/`
- Nommage : `media_YYYYMMDD_HHMMSS.tar.gz`

### 3. `restore_db.sh`
Restauration de la base de données depuis un backup.

**Usage :**
```bash
./restore_db.sh /var/www/amcd57/backups/db/amcd57_db_20251026_120000.sql.gz
```

**Caractéristiques :**
- Demande confirmation avant restauration
- Crée un backup de sécurité automatique avant restauration
- Arrête/redémarre Gunicorn automatiquement
- Recrée complètement la base de données

⚠️ **ATTENTION** : La restauration écrase TOUTES les données actuelles !

### 4. `setup_backups.sh`
Script d'installation et configuration initiale des backups.

**Usage :**
```bash
sudo ./setup_backups.sh
```

**Actions effectuées :**
- Création des répertoires de backup
- Configuration du fichier `.pgpass` pour PostgreSQL
- Attribution des permissions
- Configuration des cron jobs automatiques
- Test des scripts de backup

## ⏰ Planification automatique (Cron)

Après installation avec `setup_backups.sh`, les backups s'exécutent automatiquement :

| Script | Fréquence | Heure | Logs |
|--------|-----------|-------|------|
| `backup_db.sh` | Quotidien | 2h00 | `/var/www/amcd57/logs/backup_db.log` |
| `backup_media.sh` | Quotidien | 3h00 | `/var/www/amcd57/logs/backup_media.log` |

### Voir les cron jobs actifs
```bash
crontab -l
```

### Modifier les cron jobs
```bash
crontab -e
```

## 📦 Emplacement des backups

```
/var/www/amcd57/backups/
├── db/
│   ├── amcd57_db_20251026_020000.sql.gz
│   ├── amcd57_db_20251027_020000.sql.gz
│   └── ...
└── media/
    ├── media_20251026_030000.tar.gz
    ├── media_20251027_030000.tar.gz
    └── ...
```

## 🔍 Commandes utiles

### Lister les backups disponibles
```bash
# Backups de la base de données
ls -lh /var/www/amcd57/backups/db/

# Backups des médias
ls -lh /var/www/amcd57/backups/media/
```

### Vérifier la taille totale des backups
```bash
du -sh /var/www/amcd57/backups/
```

### Voir les logs de backup
```bash
# Logs backup DB
tail -f /var/www/amcd57/logs/backup_db.log

# Logs backup média
tail -f /var/www/amcd57/logs/backup_media.log
```

### Tester un backup manuellement
```bash
# Backup de la base de données
/var/www/amcd57/scripts/backup_db.sh

# Backup des médias
/var/www/amcd57/scripts/backup_media.sh
```

### Restaurer depuis un backup
```bash
# Lister les backups disponibles
ls -lh /var/www/amcd57/backups/db/

# Restaurer (remplacer par le nom du fichier souhaité)
/var/www/amcd57/scripts/restore_db.sh /var/www/amcd57/backups/db/amcd57_db_20251026_020000.sql.gz
```

## 🔐 Configuration PostgreSQL

Le fichier `.pgpass` est créé automatiquement par `setup_backups.sh` dans `/home/amcd/.pgpass`.

**Format :**
```
localhost:5432:amcd57_db:amcd57_user:mot_de_passe
```

**Permissions :** `600` (lecture/écriture propriétaire uniquement)

Si vous devez le modifier manuellement :
```bash
nano /home/amcd/.pgpass
chmod 600 /home/amcd/.pgpass
```

## 🧹 Rétention des backups

Les anciens backups sont automatiquement supprimés :
- **Base de données** : conservation de 30 jours
- **Fichiers média** : conservation de 60 jours

Pour modifier la rétention, éditez les scripts :
```bash
nano /var/www/amcd57/scripts/backup_db.sh
# Modifier la variable RETENTION_DAYS
```

## 🚨 Restauration d'urgence

### Scénario 1 : Restauration complète après incident

1. Identifier le backup à restaurer :
```bash
ls -lh /var/www/amcd57/backups/db/
```

2. Restaurer la base de données :
```bash
/var/www/amcd57/scripts/restore_db.sh /var/www/amcd57/backups/db/amcd57_db_YYYYMMDD_HHMMSS.sql.gz
```

3. Restaurer les médias (si nécessaire) :
```bash
cd /var/www/amcd57
sudo rm -rf media/*
sudo tar -xzf /var/www/amcd57/backups/media/media_YYYYMMDD_HHMMSS.tar.gz -C /var/www/amcd57/
sudo chown -R amcd:amcd media/
```

4. Redémarrer les services :
```bash
sudo systemctl restart gunicorn-amcd57
sudo systemctl restart nginx
```

### Scénario 2 : Copie des backups vers un autre serveur

```bash
# Depuis le serveur de production vers un serveur de stockage
rsync -avz /var/www/amcd57/backups/ user@backup-server:/path/to/backups/amcd57/
```

## 📊 Monitoring

### Vérifier que les backups s'exécutent correctement

```bash
# Vérifier les logs pour détecter des erreurs
grep -i "error\|erreur" /var/www/amcd57/logs/backup_*.log

# Vérifier la date du dernier backup
ls -lt /var/www/amcd57/backups/db/ | head -n 2
ls -lt /var/www/amcd57/backups/media/ | head -n 2
```

### Tester l'intégrité d'un backup

```bash
# Tester qu'un backup DB peut être décompressé
gunzip -t /var/www/amcd57/backups/db/amcd57_db_YYYYMMDD_HHMMSS.sql.gz

# Tester qu'un backup média peut être décompressé
tar -tzf /var/www/amcd57/backups/media/media_YYYYMMDD_HHMMSS.tar.gz > /dev/null
```

## ⚠️ Notes importantes

- Les scripts nécessitent que PostgreSQL soit configuré avec le fichier `.pgpass`
- Le script de restauration arrête Gunicorn pendant la restauration
- Un backup de sécurité est automatiquement créé avant chaque restauration
- Les backups sont stockés localement - envisagez une copie distante pour une sécurité maximale
- Testez régulièrement vos procédures de restauration !

## 🔗 Ressources

- [Documentation PostgreSQL pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- [Documentation Cron](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [DEPLOIEMENT.md](../DEPLOIEMENT.md) - Guide complet de déploiement
