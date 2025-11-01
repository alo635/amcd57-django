# 🔧 DEBUG: Problème d'upload de photo de profil

## Problème rapporté

L'ajout d'une photo de profil sur la page "Modifier mon profil" (`/membres/profil/modifier/`) ne fonctionne pas. La photo n'est pas uploadée.

## Analyse du code

### ✅ Template correctement configuré

**Fichier**: `templates/members/profil_modifier.html`

```html
<form method="POST" enctype="multipart/form-data" class="space-y-6">
    {% csrf_token %}
    <!-- ... -->
    <input type="file" id="photo" name="photo" accept="image/*"
           class="w-full px-4 py-2 border border-gray-300 rounded-lg">
```

**Vérifications**:
- ✅ `enctype="multipart/form-data"` présent sur le formulaire (ligne 17)
- ✅ `{% csrf_token %}` présent
- ✅ Input file avec `name="photo"` et `accept="image/*"`

### ✅ Vue correctement configurée

**Fichier**: `members/views.py` (lignes 180-233)

```python
@login_required
def profil_modifier(request):
    profil = request.user.profil

    if request.method == 'POST':
        # ... autres champs ...

        # Gestion de la photo
        if 'photo' in request.FILES:
            profil.photo = request.FILES['photo']

        profil.save()
        messages.success(request, "Votre profil a été mis à jour avec succès !")
        return redirect('members:dashboard')
```

**Vérifications**:
- ✅ Vérifie `'photo' in request.FILES`
- ✅ Assigne `request.FILES['photo']` au champ photo
- ✅ Appelle `profil.save()`

### ✅ Modèle correctement configuré

**Fichier**: `members/models.py` (lignes 181-186)

```python
photo = models.ImageField(
    upload_to='members/photos/',
    null=True,
    blank=True,
    verbose_name="Photo de profil"
)
```

**Vérifications**:
- ✅ Champ `ImageField` (nécessite Pillow)
- ✅ `upload_to='members/photos/'` - chemin relatif à MEDIA_ROOT
- ✅ `null=True, blank=True` - champ optionnel

### ✅ Settings Django

**Fichier**: `amcd57_project/settings.py`

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Vérifications**:
- ✅ MEDIA_URL défini
- ✅ MEDIA_ROOT défini

## Diagnostics à effectuer

### 1. Test en développement local

**Étapes**:
1. Démarrer le serveur de développement: `python manage.py runserver`
2. Se connecter à `/membres/profil/modifier/`
3. Sélectionner une photo et soumettre le formulaire
4. Vérifier dans les logs du serveur si la requête POST arrive
5. Vérifier si le fichier apparaît dans `media/members/photos/`

**Commandes de vérification locale**:
```bash
# Vérifier le répertoire media
ls -la media/members/photos/

# Suivre les logs Django en temps réel (terminal séparé)
# Logs s'affichent automatiquement avec runserver
```

### 2. Diagnostic production (VPS)

Si le problème est spécifique à la production:

#### A. Vérifier les permissions du répertoire media

```bash
# SSH sur le VPS
ssh alodev.ovh

# Vérifier les permissions
ls -la /var/www/amcd57/media/
ls -la /var/www/amcd57/media/members/

# Créer le répertoire si inexistant
mkdir -p /var/www/amcd57/media/members/photos/

# Corriger les permissions (donner ownership à l'utilisateur amcd)
sudo chown -R amcd:amcd /var/www/amcd57/media/
sudo chmod -R 755 /var/www/amcd57/media/
```

#### B. Vérifier la configuration Nginx

**Fichier**: `/etc/nginx/sites-available/amcd57`

La configuration doit servir les fichiers média:

```nginx
location /media/ {
    alias /var/www/amcd57/media/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

**Vérifier la configuration**:
```bash
# Vérifier la syntaxe Nginx
sudo nginx -t

# Voir la configuration actuelle
sudo cat /etc/nginx/sites-available/amcd57 | grep -A 5 "location /media/"
```

#### C. Vérifier les settings production

**Fichier**: `/var/www/amcd57/.env.production`

Doit contenir:
```env
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/amcd57/media
```

**Vérifier**:
```bash
cat /var/www/amcd57/.env.production | grep MEDIA
```

#### D. Vérifier les logs Gunicorn/Django en production

```bash
# Logs Gunicorn
sudo tail -n 50 /var/www/amcd57/logs/gunicorn-error.log

# Logs d'accès
sudo tail -n 50 /var/www/amcd57/logs/gunicorn-access.log

# Logs systemd
sudo journalctl -u gunicorn-amcd57 -n 50 --no-pager

# Suivre les logs en temps réel
sudo tail -f /var/www/amcd57/logs/gunicorn-error.log
```

#### E. Tester l'upload en production

1. Se connecter sur https://amcd.alodev.ovh/membres/profil/modifier/
2. Sélectionner une petite image (< 1MB pour commencer)
3. Soumettre le formulaire
4. Observer:
   - Le message de succès Django apparaît-il ?
   - La page se recharge-t-elle ?
   - Vérifier les logs immédiatement après

```bash
# Vérifier si le fichier a été créé
ls -la /var/www/amcd57/media/members/photos/
```

### 3. Problèmes courants et solutions

#### Problème 1: Permission denied

**Symptôme**: Erreur dans les logs "Permission denied" lors de l'écriture du fichier

**Solution**:
```bash
sudo chown -R amcd:amcd /var/www/amcd57/media/
sudo chmod -R 775 /var/www/amcd57/media/
```

#### Problème 2: Répertoire media n'existe pas

**Symptôme**: "No such file or directory: 'media/members/photos/'"

**Solution**:
```bash
mkdir -p /var/www/amcd57/media/members/photos/
sudo chown -R amcd:amcd /var/www/amcd57/media/
```

#### Problème 3: Pillow non installé

**Symptôme**: Erreur "No module named 'PIL'" ou problème avec ImageField

**Solution**:
```bash
cd /var/www/amcd57
source venv/bin/activate
pip install Pillow
sudo systemctl restart gunicorn-amcd57
```

#### Problème 4: Fichier trop volumineux

**Symptôme**: Upload échoue silencieusement avec grandes images

**Solution**: Augmenter les limites Nginx et Django

**Nginx** (`/etc/nginx/nginx.conf`):
```nginx
http {
    client_max_body_size 10M;
}
```

**Django** (`settings.py`):
```python
# Limite à 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760
```

Redémarrer:
```bash
sudo systemctl restart nginx
sudo systemctl restart gunicorn-amcd57
```

#### Problème 5: request.FILES vide

**Symptôme**: `'photo' not in request.FILES` même avec fichier sélectionné

**Causes possibles**:
- Attribut `enctype="multipart/form-data"` manquant sur le formulaire
- Middleware CSRF bloque la requête
- JavaScript qui intercepte le formulaire

**Debug**:
Ajouter du logging temporaire dans `members/views.py`:
```python
@login_required
def profil_modifier(request):
    if request.method == 'POST':
        print(f"DEBUG - request.FILES: {request.FILES}")
        print(f"DEBUG - 'photo' in FILES: {'photo' in request.FILES}")

        if 'photo' in request.FILES:
            print(f"DEBUG - Photo trouvée: {request.FILES['photo'].name}")
```

### 4. Test de diagnostic complet (production)

Script de test complet à exécuter sur le VPS:

```bash
#!/bin/bash
echo "=== DIAGNOSTIC UPLOAD PHOTO AMCD57 ==="
echo ""

echo "1. Vérification répertoire media"
ls -la /var/www/amcd57/media/members/photos/ 2>/dev/null || echo "❌ Répertoire n'existe pas"
echo ""

echo "2. Permissions media"
stat -c "%a %U:%G %n" /var/www/amcd57/media/ 2>/dev/null
echo ""

echo "3. Configuration Nginx media"
sudo grep -A 5 "location /media/" /etc/nginx/sites-available/amcd57
echo ""

echo "4. Variables MEDIA dans .env"
grep MEDIA /var/www/amcd57/.env.production
echo ""

echo "5. Pillow installé ?"
/var/www/amcd57/venv/bin/python -c "import PIL; print(f'Pillow version: {PIL.__version__}')" 2>/dev/null || echo "❌ Pillow non installé"
echo ""

echo "6. Dernières erreurs Gunicorn"
sudo tail -n 20 /var/www/amcd57/logs/gunicorn-error.log | grep -i "error\|exception" || echo "Pas d'erreurs récentes"
echo ""

echo "=== FIN DIAGNOSTIC ==="
```

## Checklist de résolution

- [ ] Tester upload en développement local
- [ ] Vérifier que le code fonctionne localement
- [ ] Si local OK, vérifier permissions `/var/www/amcd57/media/` sur VPS
- [ ] Vérifier que le répertoire `members/photos/` existe
- [ ] Vérifier configuration Nginx `location /media/`
- [ ] Vérifier variables MEDIA dans `.env.production`
- [ ] Vérifier que Pillow est installé dans le venv
- [ ] Tester avec une petite image (< 500KB)
- [ ] Consulter les logs Gunicorn pendant l'upload
- [ ] Si nécessaire, ajouter du logging temporaire dans la vue

## Prochaines étapes

1. **Test local immédiat**: Vérifier si le problème existe en développement
2. **Si local fonctionne**: Le problème est spécifique à la production (permissions ou configuration)
3. **Si local échoue aussi**: Problème dans le code (vérifier logique de la vue)
4. **Après diagnostic**: Appliquer la solution appropriée selon le problème identifié
