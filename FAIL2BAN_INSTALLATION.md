# 🔒 Installation et Configuration Fail2ban - AMCD57

## Vue d'ensemble

Ce guide détaille l'installation et la configuration de **Fail2ban** pour protéger le VPS AMCD57 contre les attaques brute force sur :
- **SSH** (connexion serveur)
- **Nginx** (403, 404, DoS)
- **Django Admin** (tentatives de connexion)

**Durée estimée** : 30-45 minutes
**Difficulté** : Moyenne ⭐⭐

---

## 📋 Prérequis

- Accès SSH au VPS avec sudo
- Nginx et Django déjà installés et fonctionnels
- UFW firewall actif
- Votre IP personnelle pour la whitelist

---

## 🚀 Installation

### Étape 1 : Installer Fail2ban

Sur le VPS :

```bash
# Mise à jour des paquets
sudo apt update

# Installation de Fail2ban
sudo apt install fail2ban -y

# Vérifier l'installation
fail2ban-client --version

# Vérifier le statut du service
sudo systemctl status fail2ban
```

**Résultat attendu** : `Active: active (running)`

### Étape 2 : Vérifier votre IP personnelle

Avant de configurer, identifiez votre IP pour l'ajouter à la whitelist :

```bash
# Sur votre machine locale
curl ifconfig.me
```

Notez cette IP (ex: `123.45.67.89`), vous en aurez besoin.

---

## ⚙️ Configuration

### Étape 3 : Créer le fichier de configuration principal

Fail2ban utilise `/etc/fail2ban/jail.conf` par défaut, mais on ne doit **jamais** le modifier directement. On crée un fichier `/etc/fail2ban/jail.local` qui override les paramètres par défaut.

```bash
# Créer le fichier jail.local
sudo nano /etc/fail2ban/jail.local
```

Copiez-collez la configuration suivante :

```ini
[DEFAULT]
# ===== PARAMÈTRES GLOBAUX =====

# IP à ignorer (whitelist)
# IMPORTANT : Remplacez 123.45.67.89 par VOTRE IP personnelle !
ignoreip = 127.0.0.1/8 ::1 123.45.67.89

# Durée du bannissement (secondes)
# 3600 = 1 heure
bantime  = 3600

# Période de recherche des échecs (secondes)
# 600 = 10 minutes
findtime  = 600

# Nombre max de tentatives avant bannissement
maxretry = 3

# Action à effectuer lors d'un ban
# action = %(action_)s  → Ban simple
# action = %(action_mw)s → Ban + email avec whois
# action = %(action_mwl)s → Ban + email avec whois + logs
banaction = iptables-multiport
action = %(action_)s

# ===== JAIL SSH =====
[sshd]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 3
bantime  = 3600

# ===== JAIL NGINX - 403 FORBIDDEN =====
[nginx-403]
enabled  = true
port     = http,https
filter   = nginx-403
logpath  = /var/log/nginx/access.log
maxretry = 5
findtime = 600
bantime  = 3600

# ===== JAIL NGINX - 404 NOT FOUND =====
[nginx-404]
enabled  = true
port     = http,https
filter   = nginx-404
logpath  = /var/log/nginx/access.log
maxretry = 10
findtime = 600
bantime  = 3600

# ===== JAIL NGINX - LIMIT REQUEST (DoS) =====
[nginx-limit-req]
enabled  = true
port     = http,https
filter   = nginx-limit-req
logpath  = /var/log/nginx/error.log
maxretry = 10
findtime = 60
bantime  = 600

# ===== JAIL DJANGO ADMIN =====
[django-admin]
enabled  = true
port     = http,https
filter   = django-admin
logpath  = /var/log/nginx/access.log
maxretry = 3
findtime = 600
bantime  = 3600
```

**N'oubliez pas de remplacer `123.45.67.89` par votre vraie IP !**

Sauvegardez : `Ctrl+O`, `Enter`, `Ctrl+X`

---

### Étape 4 : Créer les filtres personnalisés

Les filtres définissent les patterns regex pour détecter les tentatives d'intrusion.

#### Filtre Nginx - 403 Forbidden

```bash
sudo nano /etc/fail2ban/filter.d/nginx-403.conf
```

Contenu :

```ini
# Fail2ban filter pour Nginx 403 Forbidden
# Bloque les IPs qui reçoivent trop de 403

[Definition]

# Règle de détection
failregex = ^<HOST> -.*"(GET|POST|HEAD|PUT|DELETE|OPTIONS).*HTTP.*" 403

# Ignorer les requêtes sur certains fichiers statiques (optionnel)
ignoreregex = \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf)
```

Sauvegardez : `Ctrl+O`, `Enter`, `Ctrl+X`

#### Filtre Nginx - 404 Not Found

```bash
sudo nano /etc/fail2ban/filter.d/nginx-404.conf
```

Contenu :

```ini
# Fail2ban filter pour Nginx 404 Not Found
# Bloque les IPs qui génèrent trop de 404 (scan de vulnérabilités)

[Definition]

# Règle de détection
failregex = ^<HOST> -.*"(GET|POST|HEAD|PUT|DELETE|OPTIONS).*HTTP.*" 404

# Ignorer les 404 légitimes sur favicon, robots.txt, etc.
ignoreregex = \/favicon\.ico
              \/robots\.txt
              \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf)
```

Sauvegardez : `Ctrl+O`, `Enter`, `Ctrl+X`

#### Filtre Django Admin

```bash
sudo nano /etc/fail2ban/filter.d/django-admin.conf
```

Contenu :

```ini
# Fail2ban filter pour Django Admin
# Bloque les tentatives de connexion échouées sur /admin/

[Definition]

# Règle de détection : POST sur /admin/login/ avec 200 (échec) ou 302 (échec puis redirect)
# Django renvoie 200 avec erreur quand login échoue
failregex = ^<HOST> -.*"POST /admin/login/.*HTTP.*" (200|302)

# Ignorer les vraies connexions réussies (302 vers dashboard)
# Note : Les vrais succès sont des 302 vers /membres/dashboard/
# Les échecs sont des 302 vers /admin/login/?next=... ou 200 avec erreur
```

**Note** : Ce filtre est basique. Pour une détection plus précise, il faudrait parser les logs Django directement. Mais pour un premier niveau de protection, cela suffit.

Sauvegardez : `Ctrl+O`, `Enter`, `Ctrl+X`

---

### Étape 5 : Tester la configuration

Avant de redémarrer Fail2ban, testons que la configuration est valide :

```bash
# Tester la configuration
sudo fail2ban-client -t

# Si des erreurs apparaissent, les corriger avant de continuer
```

**Résultat attendu** : `OK: configuration test is successful`

---

### Étape 6 : Redémarrer Fail2ban

```bash
# Redémarrer Fail2ban pour appliquer la configuration
sudo systemctl restart fail2ban

# Vérifier le statut
sudo systemctl status fail2ban

# Activer au démarrage (normalement déjà activé)
sudo systemctl enable fail2ban
```

---

## ✅ Vérification

### Étape 7 : Vérifier que les jails sont actifs

```bash
# Lister tous les jails actifs
sudo fail2ban-client status

# Résultat attendu :
# Status
# |- Number of jail:      5
# `- Jail list:   sshd, nginx-403, nginx-404, nginx-limit-req, django-admin
```

Vérifier le statut détaillé d'un jail spécifique :

```bash
# Exemple pour SSH
sudo fail2ban-client status sshd

# Exemple pour Nginx 403
sudo fail2ban-client status nginx-403
```

**Informations affichées** :
- Nombre d'IPs actuellement bannies
- Nombre total de bans depuis le démarrage
- Liste des IPs bannies
- Nombre d'échecs détectés

---

## 🧪 Tests

### Test 1 : Tester le ban SSH (optionnel, à faire avec précaution)

**⚠️ ATTENTION** : Ne testez PAS depuis votre IP personnelle ! Utilisez une VM, un VPS jetable, ou un téléphone en 4G.

Depuis une **autre machine** :

```bash
# Faire 3 tentatives de connexion SSH avec un mauvais mot de passe
ssh fakeuser@VPS_IP
# (entrer un mauvais mot de passe 3 fois)
```

Après 3 échecs, l'IP doit être bannie. Sur le VPS, vérifiez :

```bash
sudo fail2ban-client status sshd
```

Vous devriez voir l'IP test dans la liste des IPs bannies.

### Test 2 : Tester le ban Nginx 404

Depuis votre navigateur ou avec curl, faire plusieurs requêtes vers des pages inexistantes :

```bash
# Depuis votre machine
for i in {1..15}; do curl -s https://amcd.alodev.ovh/page-inexistante-$i > /dev/null; done
```

⚠️ **Attention** : Si vous testez depuis votre IP personnelle, vous serez banni ! Assurez-vous d'avoir bien ajouté votre IP dans `ignoreip`.

Sur le VPS, vérifiez :

```bash
sudo fail2ban-client status nginx-404
```

### Test 3 : Débannir une IP (pour les tests)

Si vous vous êtes banni par accident :

```bash
# Débannir une IP spécifique d'un jail
sudo fail2ban-client set sshd unbanip 123.45.67.89

# Ou débannir de TOUS les jails
sudo fail2ban-client unban 123.45.67.89
```

---

## 📊 Monitoring

### Commandes utiles

```bash
# Voir les logs en temps réel
sudo tail -f /var/log/fail2ban.log

# Voir les dernières actions de ban
sudo grep "Ban" /var/log/fail2ban.log | tail -20

# Voir les statistiques de tous les jails
sudo fail2ban-client status

# Voir les IPs actuellement bannies
sudo fail2ban-client banned

# Compter le nombre total de bans
sudo grep -c "Ban" /var/log/fail2ban.log
```

### Logs Fail2ban

Les logs sont dans `/var/log/fail2ban.log` :

```bash
# Voir les 50 dernières lignes
sudo tail -50 /var/log/fail2ban.log

# Chercher les bans SSH
sudo grep "sshd.*Ban" /var/log/fail2ban.log

# Chercher les bans Nginx
sudo grep "nginx.*Ban" /var/log/fail2ban.log
```

---

## 🔧 Configuration avancée (optionnel)

### Notifications par email

Pour recevoir un email quand une IP est bannie :

1. **Installer un serveur mail local** :
   ```bash
   sudo apt install postfix mailutils
   ```

2. **Modifier jail.local** :
   ```ini
   [DEFAULT]
   # Votre email
   destemail = votre@email.com
   sender = fail2ban@amcd.alodev.ovh

   # Action avec notification
   action = %(action_mw)s
   ```

3. **Redémarrer Fail2ban** :
   ```bash
   sudo systemctl restart fail2ban
   ```

### Augmenter la durée de ban

Pour bannir plus longtemps (ex: 24 heures) :

```ini
[DEFAULT]
bantime = 86400  # 24 heures en secondes
```

### Bannissement permanent après X récidives

Créer `/etc/fail2ban/action.d/iptables-multiport-persistent.conf` :

```ini
[Definition]
actionban = iptables -I fail2ban-<name> 1 -s <ip> -j DROP
            echo "<ip>" >> /etc/fail2ban/persistent.bans

actionunban = iptables -D fail2ban-<name> -s <ip> -j DROP
              sed -i '/<ip>/d' /etc/fail2ban/persistent.bans
```

---

## ❓ Dépannage

### Fail2ban ne démarre pas

```bash
# Vérifier les erreurs dans les logs
sudo journalctl -u fail2ban -n 50

# Tester la configuration
sudo fail2ban-client -t

# Vérifier la syntaxe des filtres
sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nginx-403.conf
```

### Un jail ne fonctionne pas

```bash
# Vérifier que le logpath existe et est lisible
ls -la /var/log/nginx/access.log

# Tester le filtre avec fail2ban-regex
sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nginx-403.conf --print-all-matched

# Voir si des échecs sont détectés
sudo fail2ban-client status nginx-403
```

### Je suis banni de mon propre serveur !

Si vous n'avez plus accès SSH :

1. **Via console OVH** : Connectez-vous via la console web de OVH
2. **Débannir votre IP** :
   ```bash
   sudo fail2ban-client unban VOTRE_IP
   ```
3. **Ajouter votre IP à ignoreip** dans `/etc/fail2ban/jail.local`
4. **Redémarrer Fail2ban** :
   ```bash
   sudo systemctl restart fail2ban
   ```

---

## 📝 Checklist de validation

Avant de considérer l'installation terminée, vérifiez :

- [ ] Fail2ban installé et actif : `sudo systemctl status fail2ban`
- [ ] Fichier `/etc/fail2ban/jail.local` créé avec votre IP dans ignoreip
- [ ] 5 jails actifs : sshd, nginx-403, nginx-404, nginx-limit-req, django-admin
- [ ] Filtres personnalisés créés dans `/etc/fail2ban/filter.d/`
- [ ] Configuration testée : `sudo fail2ban-client -t` → OK
- [ ] Aucune erreur dans `/var/log/fail2ban.log`
- [ ] Test de ban réussi (depuis une IP jetable)
- [ ] Vous pouvez toujours vous connecter en SSH (IP dans whitelist)
- [ ] Fail2ban actif au démarrage : `sudo systemctl is-enabled fail2ban`

---

## 📚 Références

- **Documentation officielle** : https://www.fail2ban.org/wiki/index.php/Main_Page
- **Filtres communautaires** : https://github.com/fail2ban/fail2ban/tree/master/config/filter.d
- **DigitalOcean Guide** : https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu

---

## 🎯 Résumé des protections

Après installation complète, votre serveur est protégé contre :

| Type d'attaque | Protection | Seuil | Durée ban |
|----------------|------------|-------|-----------|
| **SSH Brute Force** | ✅ | 3 échecs / 10 min | 1 heure |
| **Nginx 403** | ✅ | 5 échecs / 10 min | 1 heure |
| **Nginx 404 (scan)** | ✅ | 10 échecs / 10 min | 1 heure |
| **Nginx DoS** | ✅ | 10 req / 1 min | 10 minutes |
| **Django Admin** | ✅ | 3 échecs / 10 min | 1 heure |

---

**Date de création** : 29 octobre 2025
**Dernière mise à jour** : 29 octobre 2025
**Version** : 1.0
**Auteur** : Équipe AMCD57
