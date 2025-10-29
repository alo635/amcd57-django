# 🔧 Guide rapide : Déboguer l'upload de photo en production

## Problème identifié

✅ **En local** : L'upload de photo fonctionne
❌ **En production** : L'upload de photo ne fonctionne pas
📊 **Logs Gunicorn** : Pas de logs visibles

**Conclusion** : Problème de configuration production (permissions, chemins, ou logs)

---

## 🚀 Étape 1 : Exécuter le script de diagnostic

Copiez le script de diagnostic sur le VPS et exécutez-le :

```bash
# Sur votre machine locale, copiez le script vers le VPS
scp scripts/diagnostic_photo_production.sh alodev.ovh:/var/www/amcd57/

# Connectez-vous au VPS
ssh alodev.ovh

# Rendez le script exécutable
chmod +x /var/www/amcd57/diagnostic_photo_production.sh

# Exécutez le script
sudo /var/www/amcd57/diagnostic_photo_production.sh
```

Le script va vérifier :
- ✅ Existence des répertoires media
- ✅ Permissions des répertoires
- ✅ Test d'écriture (CRITIQUE)
- ✅ Utilisateur Gunicorn
- ✅ Configuration Nginx
- ✅ Variables .env
- ✅ Installation de Pillow
- ✅ Logs Gunicorn et systemd

---

## 🔍 Étape 2 : Interpréter les résultats

### Scénario A : Test d'écriture échoue ❌

Si vous voyez : **"❌ IMPOSSIBLE D'ÉCRIRE dans media/members/photos/"**

**Solution** :
```bash
# Corriger les permissions
sudo chown -R amcd:amcd /var/www/amcd57/media/
sudo chmod -R 775 /var/www/amcd57/media/

# Vérifier
ls -la /var/www/amcd57/media/members/
```

Puis redémarrer Gunicorn :
```bash
sudo systemctl restart gunicorn-amcd57
```

### Scénario B : Répertoire photos n'existe pas ⚠️

Le script le crée automatiquement, mais corrigez ensuite les permissions :
```bash
sudo chown -R amcd:amcd /var/www/amcd57/media/
sudo chmod -R 775 /var/www/amcd57/media/
```

### Scénario C : Configuration Nginx manquante ❌

Si la section `location /media/` n'existe pas dans Nginx :

```bash
# Éditez la config Nginx
sudo nano /etc/nginx/sites-available/amcd57
```

Ajoutez (ou vérifiez) :
```nginx
location /media/ {
    alias /var/www/amcd57/media/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

Puis :
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Scénario D : Pillow non installé ❌

```bash
cd /var/www/amcd57
source venv/bin/activate
pip install Pillow
sudo systemctl restart gunicorn-amcd57
```

---

## 🧪 Étape 3 : Tester l'upload avec monitoring en temps réel

### Dans un terminal SSH (1) - Suivre les logs

```bash
# Terminal 1 : Suivre les logs systemd en temps réel
sudo journalctl -u gunicorn-amcd57 -f
```

### Dans un autre terminal SSH (2) - Vérifier le répertoire

```bash
# Terminal 2 : Surveiller le répertoire media
watch -n 1 'ls -lah /var/www/amcd57/media/members/photos/'
```

### Dans votre navigateur

1. Allez sur https://amcd.alodev.ovh/membres/profil/modifier/
2. Connectez-vous
3. Sélectionnez une **petite** image (< 500 KB)
4. Cliquez sur "Enregistrer"
5. Observez les deux terminaux SSH

---

## 📋 Étape 4 : Analyser les logs de debug

Les logs de debug que j'ai ajoutés dans le code devraient apparaître dans les logs Gunicorn ou systemd :

```
=== DEBUG PHOTO UPLOAD ===
request.FILES keys: ['photo']
'photo' in request.FILES: True
Photo filename: mon-image.jpg
Photo size: 245678 bytes
Photo content type: image/jpeg
=========================
```

**Si vous ne voyez PAS ces logs** :
- Les logs ne sont peut-être pas au bon endroit
- Gunicorn redirige peut-être stdout ailleurs
- Il faut vérifier la config systemd du service Gunicorn

---

## 🔧 Étape 5 : Vérifier la configuration systemd de Gunicorn

```bash
# Voir la config du service
sudo systemctl cat gunicorn-amcd57
```

Vérifiez que les logs sont bien configurés :
```ini
[Service]
StandardOutput=append:/var/www/amcd57/logs/gunicorn-access.log
StandardError=append:/var/www/amcd57/logs/gunicorn-error.log
```

Si les chemins sont différents ou absents, les logs sont peut-être ailleurs.

**Alternatives pour trouver les logs** :
```bash
# Chercher tous les fichiers de logs
find /var/www/amcd57 -name "*.log" -type f

# Chercher dans /var/log
sudo find /var/log -name "*gunicorn*" -o -name "*amcd*"

# Voir les logs systemd (toujours disponibles)
sudo journalctl -u gunicorn-amcd57 --since "10 minutes ago"
```

---

## 🎯 Étape 6 : Solutions selon les symptômes

### Symptôme : Message de succès Django mais pas de photo

**Cause probable** : Permissions - le fichier est rejeté silencieusement

**Solution** :
```bash
sudo chown -R amcd:amcd /var/www/amcd57/media/
sudo chmod -R 775 /var/www/amcd57/media/
sudo systemctl restart gunicorn-amcd57
```

### Symptôme : Page ne se recharge pas / erreur 500

**Cause probable** : Exception Python non catchée

**Solution** : Vérifier les logs systemd
```bash
sudo journalctl -u gunicorn-amcd57 -n 50 --no-pager | grep -i error
```

### Symptôme : Photo uploadée mais ne s'affiche pas

**Cause probable** : Nginx ne sert pas les fichiers media

**Solution** : Vérifier la config Nginx et les permissions
```bash
# Tester l'accès direct à un fichier media existant
curl -I https://amcd.alodev.ovh/media/blog/articles/2022/09/P1030409.jpg

# Devrait retourner 200 OK
```

---

## 📞 Si rien ne fonctionne : Debugging manuel

### Option 1 : Upload via l'admin Django

Testez d'abord l'upload via l'interface admin :

1. Allez sur https://amcd.alodev.ovh/admin/
2. Connectez-vous en tant que superuser
3. Allez dans **Members → Profils membres**
4. Choisissez un profil
5. Uploadez une photo via le champ "Photo de profil"

Si ça fonctionne en admin mais pas en frontend → problème dans le template ou la vue frontend.
Si ça ne fonctionne pas non plus → problème système (permissions).

### Option 2 : Tester directement avec Python

```bash
ssh alodev.ovh
cd /var/www/amcd57
source venv/bin/activate
python manage.py shell
```

```python
from members.models import ProfilMembre
from django.core.files.uploadedfile import SimpleUploadedFile

# Récupérer un profil
profil = ProfilMembre.objects.first()

# Créer un fichier de test
with open('/tmp/test.txt', 'w') as f:
    f.write('test')

# Tester l'upload
with open('/tmp/test.txt', 'rb') as f:
    profil.photo.save('test.txt', f, save=True)

# Vérifier le chemin
print(profil.photo.path)
print(profil.photo.url)

# Le fichier devrait exister
import os
print(os.path.exists(profil.photo.path))
```

Si cette commande échoue, vous verrez l'erreur exacte (permission denied, directory not found, etc.).

---

## ✅ Checklist finale

Avant de déclarer victoire, vérifiez :

- [ ] Test d'écriture réussit : `echo "test" > /var/www/amcd57/media/members/photos/test.txt`
- [ ] Permissions correctes : `ls -la /var/www/amcd57/media/` montre `amcd:amcd`
- [ ] Répertoire existe : `/var/www/amcd57/media/members/photos/`
- [ ] Nginx configuré : `location /media/` présent et testé
- [ ] Pillow installé : `pip list | grep -i pillow` dans le venv
- [ ] Service redémarré : `sudo systemctl restart gunicorn-amcd57`
- [ ] Logs accessibles : `sudo journalctl -u gunicorn-amcd57 -f` fonctionne
- [ ] Upload fonctionne via admin Django
- [ ] Upload fonctionne via frontend
- [ ] Photo s'affiche dans le profil

---

## 🧹 Après résolution : Nettoyage

Une fois le problème résolu, retirer les logs de debug :

```bash
# Sur votre machine locale
# Je retirerai les lignes de debug dans members/views.py
# Puis git commit et push
# Puis sur le VPS : git pull + restart gunicorn
```

---

## 📚 Références

- [DEBUG_PHOTO_UPLOAD.md](DEBUG_PHOTO_UPLOAD.md) - Documentation complète du problème
- [DEPLOIEMENT.md](DEPLOIEMENT.md) - Guide de déploiement complet
- Django docs : https://docs.djangoproject.com/en/5.0/topics/files/
