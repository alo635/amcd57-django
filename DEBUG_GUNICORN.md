# 🔧 DEBUG: Problème de démarrage Gunicorn

## Erreur observée

```
gunicorn-amcd57.service: Main process exited, code=exited, status=255/EXCEPTION
gunicorn-amcd57.service: Failed with result 'exit-code'
```

## Étapes de diagnostic

### 1. Vérifier les logs Gunicorn détaillés

```bash
# Vérifier les logs d'erreur Gunicorn
sudo tail -n 50 /var/www/amcd57/logs/gunicorn-error.log

# Si le fichier n'existe pas, vérifier les logs systemd
sudo journalctl -u gunicorn-amcd57 -n 50 --no-pager
```

### 2. Vérifier les permissions

```bash
# Le répertoire logs existe-t-il ?
ls -la /var/www/amcd57/logs/

# Permissions correctes ?
sudo chown -R amcd:amcd /var/www/amcd57/logs/
sudo chmod -R 755 /var/www/amcd57/logs/
```

### 3. Tester Gunicorn manuellement

```bash
cd /var/www/amcd57
source venv/bin/activate

# Tester Gunicorn directement (avec variables d'environnement)
export DJANGO_SETTINGS_MODULE=amcd57_project.settings
export DJANGO_CONFIGURATION=Production

gunicorn amcd57_project.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 3 \
  --log-level debug
```

**Observation** : Cette commande devrait afficher les erreurs réelles.

### 4. Problèmes courants

#### A. Le fichier socket ou PID existe déjà

```bash
# Supprimer les fichiers socket/PID potentiels
sudo rm -f /var/www/amcd57/gunicorn.sock
sudo rm -f /var/www/amcd57/gunicorn.pid
```

#### B. L'utilisateur/groupe n'existe pas

```bash
# Vérifier que l'utilisateur amcd existe
id amcd

# Si l'utilisateur n'existe pas, le créer
sudo useradd -m -s /bin/bash amcd
sudo chown -R amcd:amcd /var/www/amcd57
```

#### C. Variables d'environnement manquantes

Vérifier le fichier de service systemd :

```bash
sudo nano /etc/systemd/system/gunicorn-amcd57.service
```

Le fichier doit contenir :

```ini
[Unit]
Description=Gunicorn daemon for AMCD57 Django application
After=network.target

[Service]
Type=notify
User=amcd
Group=amcd
WorkingDirectory=/var/www/amcd57
EnvironmentFile=/var/www/amcd57/.env.production

ExecStart=/var/www/amcd57/venv/bin/gunicorn \
          --config /var/www/amcd57/gunicorn_config.py \
          amcd57_project.wsgi:application

ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### D. Vérifier le fichier gunicorn_config.py

```bash
cat /var/www/amcd57/gunicorn_config.py
```

**Problème possible** : Le fichier spécifie `user = "amcd"` et `group = "amcd"`. Si Gunicorn est lancé par systemd avec User=amcd, il n'a PAS besoin (et ne peut pas) changer d'utilisateur.

**Solution** : Commenter ou supprimer les lignes user/group dans gunicorn_config.py :

```python
# user = "amcd"      # COMMENTER CETTE LIGNE
# group = "amcd"     # COMMENTER CETTE LIGNE
```

#### E. Vérifier que le virtualenv contient gunicorn

```bash
/var/www/amcd57/venv/bin/gunicorn --version
```

Si gunicorn n'est pas installé :

```bash
cd /var/www/amcd57
source venv/bin/activate
pip install gunicorn
```

### 5. Relancer après corrections

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Réinitialiser l'état failed
sudo systemctl reset-failed gunicorn-amcd57

# Redémarrer
sudo systemctl restart gunicorn-amcd57

# Vérifier le statut
sudo systemctl status gunicorn-amcd57

# Suivre les logs en temps réel
sudo journalctl -u gunicorn-amcd57 -f
```

## Solutions par type d'erreur

### Erreur "Permission denied" dans les logs

```bash
sudo chown -R amcd:amcd /var/www/amcd57
sudo chmod -R 755 /var/www/amcd57
sudo chmod -R 775 /var/www/amcd57/logs
```

### Erreur "No module named 'amcd57_project'"

```bash
cd /var/www/amcd57
source venv/bin/activate
pip install -r requirements-prod.txt
```

### Erreur "Can't switch to 'amcd' user"

Éditer `/var/www/amcd57/gunicorn_config.py` et commenter :

```python
# user = "amcd"
# group = "amcd"
```

Car systemd gère déjà l'utilisateur.

### Erreur liée à SECRET_KEY ou variables d'environnement

Vérifier `/var/www/amcd57/.env.production` :

```bash
cat /var/www/amcd57/.env.production
```

Doit contenir au minimum :

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,amcd.alodev.ovh,www.amcd57.fr
DATABASE_URL=postgresql://amcd_user:your-password@localhost:5432/amcd_db
```

## Checklist complète

- [ ] Répertoire `/var/www/amcd57/logs/` existe avec bonnes permissions
- [ ] Utilisateur `amcd` existe
- [ ] Fichier `.env.production` existe et contient toutes les variables
- [ ] Gunicorn installé dans le virtualenv
- [ ] Lignes `user` et `group` commentées dans `gunicorn_config.py`
- [ ] Service systemd correctement configuré
- [ ] Test manuel de gunicorn fonctionne
