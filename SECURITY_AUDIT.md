# 🔒 Audit de Sécurité AMCD57

## 📊 Résumé Exécutif

**Date de l'audit** : 26 octobre 2025
**Version Django** : 5.0
**Environnement** : Production (VPS OVH)
**URL** : https://amcd.alodev.ovh

### Score de sécurité actuel

| Catégorie | Statut | Priorité |
|-----------|--------|----------|
| HTTPS/SSL | ✅ Configuré | - |
| SECRET_KEY | ⚠️ À améliorer | 🔴 Critique |
| DEBUG Mode | ⚠️ Vérifier production | 🔴 Critique |
| ALLOWED_HOSTS | ⚠️ À configurer | 🔴 Critique |
| HSTS | ❌ Non configuré | 🟡 Important |
| Secure Cookies | ❌ Non configuré | 🟡 Important |
| CSRF Protection | ✅ Activé | - |
| SQL Injection | ✅ Protégé (ORM) | - |
| XSS Protection | ✅ Protégé (templates) | - |
| File Upload | ⚠️ À sécuriser | 🟡 Important |

---

## 🚨 Problèmes Critiques (À corriger immédiatement)

### 1. SECRET_KEY faible ⚠️

**Problème actuel** :
```python
# settings.py
SECRET_KEY = config('SECRET_KEY', default='django-insecure-CHANGE-THIS-IN-PRODUCTION')
```

**Risque** :
- Clé par défaut ou trop courte
- Vulnérabilité aux attaques de session hijacking
- Compromission des tokens CSRF
- Déchiffrement des données sensibles

**Solution** :

Sur le **VPS**, générer une vraie SECRET_KEY :

```bash
# SSH sur le VPS
ssh alodev.ovh

# Générer une SECRET_KEY sécurisée
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copier la clé générée (50+ caractères aléatoires), puis :

```bash
# Éditer le .env
nano /var/www/amcd57/.env
```

Remplacer la ligne SECRET_KEY par la nouvelle :
```env
SECRET_KEY=votre-super-longue-cle-aleatoire-generee-ici-50-caracteres-minimum
```

Redémarrer Gunicorn :
```bash
sudo systemctl restart gunicorn-amcd57
```

---

### 2. DEBUG=True en production ⚠️

**Problème actuel** :
```python
DEBUG = config('DEBUG', default=True, cast=bool)
```

**Risque** :
- Exposition des traces d'erreurs complètes (stacktraces)
- Révélation de la structure du code
- Affichage des variables sensibles
- Performance dégradée

**Solution** :

Sur le **VPS** :

```bash
nano /var/www/amcd57/.env
```

S'assurer que :
```env
DEBUG=False
```

**⚠️ TRÈS IMPORTANT : Vérifier après redémarrage** :

```bash
# Redémarrer
sudo systemctl restart gunicorn-amcd57

# Vérifier dans les logs
sudo journalctl -u gunicorn-amcd57 -n 20 --no-pager | grep DEBUG

# Ou tester via Django shell
cd /var/www/amcd57
source venv/bin/activate
python manage.py shell
>>> from django.conf import settings
>>> print(f"DEBUG = {settings.DEBUG}")
>>> # Doit afficher: DEBUG = False
>>> quit()
```

---

### 3. ALLOWED_HOSTS non configuré ⚠️

**Problème actuel** :
```python
# settings.py (code local)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

**Risque** :
- Vulnérabilité aux attaques Host Header
- Possibilité de cache poisoning
- Risque de phishing

**Solution** :

Modifier `settings.py` pour lire depuis `.env` :

```python
# settings.py
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```

Sur le **VPS**, dans `.env` :
```env
ALLOWED_HOSTS=amcd.alodev.ovh,www.amcd.alodev.ovh,localhost,127.0.0.1
```

---

## 🟡 Problèmes Importants (À corriger rapidement)

### 4. HSTS non configuré

**Problème** : HTTP Strict Transport Security non activé

**Risque** :
- Possibilité d'attaques man-in-the-middle
- Utilisateurs peuvent accéder en HTTP non sécurisé

**Solution** :

Ajouter dans `settings.py` :

```python
# Sécurité HTTPS (uniquement si SSL configuré)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

**⚠️ ATTENTION** : N'activez ceci que si :
1. Votre certificat SSL est correctement installé
2. Tout le site fonctionne en HTTPS
3. Vous avez testé l'accès HTTPS

---

### 5. Cookies non sécurisés

**Problème** : SESSION_COOKIE_SECURE et CSRF_COOKIE_SECURE = False

**Risque** :
- Vol de cookies de session via HTTP
- Interception du token CSRF

**Solution** : Voir section HSTS ci-dessus (même correction)

---

### 6. Upload de fichiers

**Problème actuel** :
- Pas de limitation de taille explicite
- Pas de validation de type MIME stricte
- Pas de scan antivirus

**Risques** :
- Upload de fichiers malveillants
- Déni de service (fichiers énormes)
- Exécution de code si mauvaise configuration serveur

**Solutions** :

#### A. Limiter la taille des uploads

Dans `settings.py` :
```python
# Limite d'upload : 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
```

#### B. Valider les types de fichiers

Dans `members/models.py`, améliorer la validation :

```python
from django.core.validators import FileExtensionValidator

class ProfilMembre(models.Model):
    photo = models.ImageField(
        upload_to='members/photos/',
        null=True,
        blank=True,
        verbose_name="Photo de profil",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp']
            )
        ]
    )
```

#### C. Configuration Nginx

Dans `/etc/nginx/sites-available/amcd57` :

```nginx
# Limite la taille des uploads
client_max_body_size 10M;
```

---

## ✅ Points Positifs (Déjà sécurisés)

### 1. Protection CSRF ✅
- `CsrfViewMiddleware` activé
- Tokens CSRF dans tous les formulaires
- Protection contre les attaques Cross-Site Request Forgery

### 2. Protection SQL Injection ✅
- Utilisation de l'ORM Django
- Pas de requêtes SQL brutes non paramétrées
- Validation automatique des entrées

### 3. Protection XSS ✅
- Auto-escape activé dans les templates
- Filtrage des balises HTML dangereuses
- `{% csrf_token %}` correctement utilisé

### 4. SSL/TLS configuré ✅
- Certificat Let's Encrypt valide
- HTTPS fonctionnel
- Redirection HTTP → HTTPS configurée dans Nginx

### 5. Authentification sécurisée ✅
- django-allauth avec bonnes pratiques
- Mots de passe hashés (PBKDF2)
- Protection contre le brute force (rate limiting possible)

### 6. Fichiers sensibles protégés ✅
- `.env` dans `.gitignore`
- `db.sqlite3` non versionné
- `media/` non versionné
- Secrets non exposés dans le code

---

## 🔐 Recommandations Supplémentaires

### 1. Variables d'environnement

**À ajouter dans `.env` production** :

```env
# Sécurité
SECRET_KEY=<clé-générée-50-caracteres-minimum>
DEBUG=False
ALLOWED_HOSTS=amcd.alodev.ovh,www.amcd.alodev.ovh

# Base de données (si PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost/dbname

# Email (pour notifications sécurisées)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=votre@email.com
# EMAIL_HOST_PASSWORD=mot-de-passe-app
# EMAIL_USE_TLS=True

# Media
MEDIA_ROOT=/var/www/amcd57/media
MEDIA_URL=/media/
```

---

### 2. Firewall (UFW)

Sur le **VPS**, vérifier le firewall :

```bash
# Vérifier le statut
sudo ufw status

# Si pas activé, configurer :
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

### 3. Fail2ban (Protection brute force)

**Installer Fail2ban** pour bloquer les attaques par force brute :

```bash
# Installer
sudo apt install fail2ban

# Configurer
sudo nano /etc/fail2ban/jail.local
```

Ajouter :
```ini
[django-auth]
enabled = true
filter = django-auth
logpath = /var/www/amcd57/logs/gunicorn-error.log
maxretry = 5
bantime = 3600
```

Créer le filtre :
```bash
sudo nano /etc/fail2ban/filter.d/django-auth.conf
```

```ini
[Definition]
failregex = ^.* "POST .*/accounts/login/.* HTTP/.*" 200
ignoreregex =
```

Redémarrer :
```bash
sudo systemctl restart fail2ban
sudo fail2ban-client status
```

---

### 4. Backups chiffrés

Améliorer les scripts de backup pour chiffrer les données sensibles :

```bash
# Backup chiffré de la base de données
pg_dump amcd57_db | gpg --encrypt --recipient admin@amcd57.fr > backup.sql.gpg
```

---

### 5. Logs de sécurité

Monitorer les logs pour détecter les activités suspectes :

```bash
# Surveiller les tentatives de connexion admin
sudo tail -f /var/www/amcd57/logs/gunicorn-access.log | grep "POST.*admin.*login"

# Surveiller les erreurs 404 (possibles scans)
sudo tail -f /var/www/amcd57/logs/gunicorn-access.log | grep " 404 "

# Surveiller les erreurs 500 (problèmes applicatifs)
sudo tail -f /var/www/amcd57/logs/gunicorn-error.log
```

---

### 6. Mises à jour régulières

```bash
# Mettre à jour les dépendances Python
cd /var/www/amcd57
source venv/bin/activate
pip list --outdated

# Mettre à jour Django (avec tests !)
pip install --upgrade django

# Mettre à jour le système
sudo apt update && sudo apt upgrade
```

---

### 7. Admin Django sécurisé

**Changer l'URL de l'admin** :

Dans `amcd57_project/urls.py` :

```python
# Au lieu de /admin/, utiliser une URL secrète
urlpatterns = [
    path('gestion-securisee-amcd57/', admin.site.urls),  # URL secrète
    # ...
]
```

Puis redémarrer Gunicorn.

**Nouvelle URL admin** : https://amcd.alodev.ovh/gestion-securisee-amcd57/

---

### 8. Rate Limiting

Ajouter `django-ratelimit` pour limiter les requêtes :

```bash
pip install django-ratelimit
```

Dans les vues sensibles :

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # ...
```

---

## 📋 Checklist de Sécurité Production

### Critique (À faire immédiatement)
- [ ] Générer et configurer une vraie SECRET_KEY (50+ caractères)
- [ ] Vérifier que DEBUG=False en production
- [ ] Configurer ALLOWED_HOSTS correctement
- [ ] Tester que le site fonctionne après ces changements

### Important (À faire rapidement)
- [ ] Activer HSTS et cookies sécurisés
- [ ] Limiter la taille des uploads (10 MB)
- [ ] Valider les types de fichiers uploadés
- [ ] Configurer le firewall UFW
- [ ] Changer l'URL de l'admin Django

### Recommandé (À faire bientôt)
- [ ] Installer et configurer Fail2ban
- [ ] Mettre en place des backups chiffrés
- [ ] Configurer un monitoring des logs
- [ ] Planifier les mises à jour régulières
- [ ] Ajouter rate limiting sur les formulaires

---

## 🧪 Tests de Sécurité

### Test 1 : Vérifier DEBUG en production

```bash
# Sur le VPS
curl -I https://amcd.alodev.ovh/page-qui-nexiste-pas

# Ne doit PAS afficher de stacktrace Django
# Doit afficher une page 404 générique
```

### Test 2 : Vérifier HTTPS

```bash
# Tester la redirection HTTP → HTTPS
curl -I http://amcd.alodev.ovh

# Doit retourner un code 301 ou 302 vers HTTPS
```

### Test 3 : Vérifier les headers de sécurité

```bash
curl -I https://amcd.alodev.ovh

# Vérifier la présence de :
# Strict-Transport-Security: max-age=31536000
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
```

### Test 4 : Scanner de vulnérabilités

Utiliser des outils en ligne :
- **SSL Labs** : https://www.ssllabs.com/ssltest/analyze.html?d=amcd.alodev.ovh
- **Security Headers** : https://securityheaders.com/?q=amcd.alodev.ovh
- **Mozilla Observatory** : https://observatory.mozilla.org/analyze/amcd.alodev.ovh

---

## 📞 En cas d'incident de sécurité

### Procédure d'urgence

1. **Isoler le problème**
   ```bash
   sudo systemctl stop gunicorn-amcd57
   sudo systemctl stop nginx
   ```

2. **Analyser les logs**
   ```bash
   sudo tail -n 500 /var/www/amcd57/logs/gunicorn-error.log
   sudo tail -n 500 /var/log/nginx/error.log
   ```

3. **Restaurer depuis backup**
   ```bash
   # Restaurer la BDD depuis backup
   python manage.py loaddata /path/to/backup.json
   ```

4. **Changer les secrets**
   - Générer nouvelle SECRET_KEY
   - Changer mots de passe admin
   - Révoquer sessions actives

5. **Redémarrer les services**
   ```bash
   sudo systemctl start gunicorn-amcd57
   sudo systemctl start nginx
   ```

---

## 📚 Ressources

- [Django Security Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)
- [Let's Encrypt Best Practices](https://letsencrypt.org/docs/)

---

**Document généré le** : 26 octobre 2025
**Prochaine révision** : 26 janvier 2026 (tous les 3 mois)
