# 🚨 Correctifs de Sécurité Rapides - À appliquer MAINTENANT

## ⏱️ Temps estimé : 10 minutes

Ces 3 actions CRITIQUES doivent être appliquées immédiatement sur le serveur de production.

---

## 1️⃣ Générer une vraie SECRET_KEY (2 min)

**Sur le VPS** :

```bash
ssh alodev.ovh
cd /var/www/amcd57

# Générer une SECRET_KEY sécurisée
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Copier la clé générée**, puis :

```bash
nano .env
```

Remplacer la ligne SECRET_KEY par :
```env
SECRET_KEY=<LA_CLE_GENEREE_COLLEE_ICI>
```

Sauvegarder (Ctrl+O, Enter, Ctrl+X).

---

## 2️⃣ Vérifier DEBUG=False (1 min)

Toujours dans `.env`, vérifier :

```bash
cat .env | grep DEBUG
```

Doit afficher :
```env
DEBUG=False
```

Si ce n'est pas le cas :
```bash
nano .env
```

Changer à :
```env
DEBUG=False
```

---

## 3️⃣ Configurer ALLOWED_HOSTS (2 min)

Dans `.env`, ajouter :

```bash
nano .env
```

Ajouter cette ligne :
```env
ALLOWED_HOSTS=amcd.alodev.ovh,www.amcd.alodev.ovh,localhost,127.0.0.1
```

---

## 4️⃣ Mettre à jour le code (3 min)

```bash
# Pull les changements de sécurité
git pull

# Vérifier que le settings.py a les nouveaux paramètres
grep "SECURE_SSL_REDIRECT" amcd57_project/settings.py

# Devrait afficher : SECURE_SSL_REDIRECT = True
```

---

## 5️⃣ Redémarrer Gunicorn (1 min)

```bash
sudo systemctl restart gunicorn-amcd57
sudo systemctl status gunicorn-amcd57
```

Vérifier que le statut est **active (running)**.

---

## 6️⃣ Vérification (1 min)

```bash
# Vérifier que DEBUG=False en production
source venv/bin/activate
python manage.py shell
```

```python
from django.conf import settings
print(f"DEBUG = {settings.DEBUG}")  # Doit afficher False
print(f"SECRET_KEY length = {len(settings.SECRET_KEY)}")  # Doit afficher 50+
print(f"ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
quit()
```

**Tester le site** : https://amcd.alodev.ovh

---

## ✅ Checklist Rapide

- [ ] SECRET_KEY générée et configurée (50+ caractères)
- [ ] DEBUG=False dans .env
- [ ] ALLOWED_HOSTS configuré
- [ ] Code mis à jour (`git pull`)
- [ ] Gunicorn redémarré
- [ ] Site accessible et fonctionnel
- [ ] Vérification dans Django shell OK

---

## 📊 Vérifier que c'est bien sécurisé

```bash
# Depuis votre machine locale, tester :
curl -I https://amcd.alodev.ovh

# Doit afficher les headers de sécurité :
# Strict-Transport-Security: max-age=31536000
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
```

---

## 🆘 En cas de problème

Si le site ne fonctionne plus après les changements :

```bash
# Voir les logs
sudo journalctl -u gunicorn-amcd57 -n 50 --no-pager

# Vérifier le fichier .env
cat .env

# Redémarrer Nginx également
sudo systemctl restart nginx
```

Si ça ne fonctionne toujours pas, **temporairement** :
```bash
nano .env
# Remettre DEBUG=True temporairement pour voir l'erreur
# Redémarrer Gunicorn
# Aller sur https://amcd.alodev.ovh pour voir l'erreur
# Corriger le problème
# Remettre DEBUG=False
```

---

## 📖 Pour aller plus loin

Voir [SECURITY_AUDIT.md](SECURITY_AUDIT.md) pour :
- Fail2ban (protection brute force)
- Changer l'URL de l'admin
- Monitoring des logs
- Tests de sécurité complets
