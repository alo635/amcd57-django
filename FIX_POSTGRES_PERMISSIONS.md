# 🔧 FIX: Permission denied for schema public

## Problème

Erreur lors de `python manage.py migrate` :
```
django.db.migrations.exceptions.MigrationSchemaMissing: Unable to create the django_migrations table (permission denied for schema public
```

## Cause

L'utilisateur PostgreSQL `amcd_user` n'a pas les permissions nécessaires pour créer des tables dans le schéma `public` de la base de données.

## Solution

Connectez-vous au serveur PostgreSQL en tant que superutilisateur et accordez les permissions nécessaires :

### Étape 1 : Se connecter à PostgreSQL en tant que postgres

```bash
sudo -u postgres psql
```

### Étape 2 : Se connecter à la base de données amcd_db

```sql
\c amcd_db
```

### Étape 3 : Accorder tous les privilèges sur le schéma public

```sql
-- Accorder tous les privilèges sur le schéma public
GRANT ALL ON SCHEMA public TO amcd_user;

-- Accorder les privilèges de création de tables
GRANT CREATE ON SCHEMA public TO amcd_user;

-- Accorder tous les privilèges sur toutes les tables existantes
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO amcd_user;

-- Accorder tous les privilèges sur toutes les séquences (pour les auto-increment)
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO amcd_user;

-- Définir les privilèges par défaut pour les futures tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO amcd_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO amcd_user;

-- Faire de amcd_user le propriétaire du schéma (optionnel mais recommandé)
ALTER SCHEMA public OWNER TO amcd_user;
```

### Étape 4 : Vérifier les permissions

```sql
-- Vérifier les permissions sur le schéma
\dn+

-- Vérifier que amcd_user est bien créé
\du
```

### Étape 5 : Quitter PostgreSQL

```sql
\q
```

### Étape 6 : Retester la migration Django

```bash
cd /var/www/amcd57
source venv/bin/activate
python manage.py migrate
```

## Alternative : Recréer la base de données avec les bonnes permissions

Si les commandes ci-dessus ne fonctionnent pas, vous pouvez recréer la base de données proprement :

```bash
sudo -u postgres psql
```

```sql
-- Supprimer la base existante
DROP DATABASE IF EXISTS amcd_db;

-- Recréer la base avec amcd_user comme propriétaire
CREATE DATABASE amcd_db OWNER amcd_user;

-- Se connecter à la nouvelle base
\c amcd_db

-- Accorder tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE amcd_db TO amcd_user;
GRANT ALL ON SCHEMA public TO amcd_user;
ALTER SCHEMA public OWNER TO amcd_user;

-- Quitter
\q
```

Puis relancer la migration :

```bash
cd /var/www/amcd57
source venv/bin/activate
python manage.py migrate
```

## Vérification finale

Après la migration, vérifiez que les tables sont bien créées :

```bash
sudo -u postgres psql -d amcd_db
```

```sql
-- Lister toutes les tables
\dt

-- Vous devriez voir :
-- django_migrations
-- auth_user
-- auth_group
-- blog_article
-- events_evenement
-- etc.
```

## Pourquoi ce problème ?

Dans PostgreSQL 15+, par défaut, le schéma `public` n'accorde plus automatiquement les privilèges `CREATE` aux utilisateurs non-superutilisateurs pour des raisons de sécurité. Il faut donc les accorder explicitement.

## Prévention

Lors de la création d'un nouvel utilisateur PostgreSQL pour Django, toujours :

```sql
CREATE DATABASE ma_base OWNER mon_user;
\c ma_base
GRANT ALL ON SCHEMA public TO mon_user;
ALTER SCHEMA public OWNER TO mon_user;
```
