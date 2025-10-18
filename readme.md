# 🛩️ AMCD57 - Site Web du Club d'Aéromodélisme

Site web moderne du club d'aéromodélisme AMCD57 de Jarny (Grand Est, France).

Migration complète d'un site WordPress vers une stack Django moderne pour obtenir un contrôle total, de meilleures performances et une meilleure évolutivité.

## 📋 Fonctionnalités

### Phase 1 - Site de base (En cours)

- ✅ Pages statiques (Accueil, Contact, Qui sommes-nous, etc.)
- 🚧 **Blog** : Articles avec catégories, tags et commentaires
- 🚧 **Système d'événements** : Réunions, sorties, vols avec inscriptions
- 🚧 **Espace membre** : Authentification, profils, espace bureau
- 🚧 **Widget météo** : Conditions de vol en temps réel (Jarny, France)
- 🚧 **Liens web** : Annuaire organisé par catégories
- 🚧 **Formulaire de contact** : Avec sauvegarde en base de données

### Phase 2 - E-commerce (Futur)

- 🔮 Boutique en ligne (pièces, équipements, adhésions)
- 🔮 Gestion des cotisations
- 🔮 Paiement en ligne sécurisé

## 🛠️ Stack Technique

### Backend

- **Django 5.0** - Framework web Python
- **django-allauth** - Système d'authentification
- **PostgreSQL** (production) / **SQLite** (développement)

### Frontend

- **Templates Django** - Système de templates
- **Tailwind CSS** - Framework CSS moderne (à venir)
- **HTMX/Alpine.js** - Interactivité légère (à venir)

### APIs

- **OpenWeatherMap** - Météo en temps réel (à venir)

## 🚀 Installation & Développement

### Prérequis

- Python 3.13+
- pip
- virtualenv

### Installation

```bash
# Cloner le repo
git clone https://github.com/TON-USERNAME/amcd57-django.git
cd amcd57-django

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env
# Éditer .env avec tes variables

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```

Le site sera accessible sur : http://127.0.0.1:8000/

### Variables d'environnement (.env)

```env
SECRET_KEY=votre-cle-secrete-django
DEBUG=True
OPENWEATHER_API_KEY=votre-cle-api
```

## 📁 Structure du Projet

```
amcd57-django/
├── amcd57_project/       # Configuration Django
├── core/                 # Pages statiques et contenu principal
├── blog/                 # Articles et catégories
├── events/               # Système d'événements
├── members/              # Profils et authentification
├── weblinks/             # Annuaire de liens
├── templates/            # Templates HTML
├── static/               # CSS, JS, images
├── media/                # Uploads utilisateurs
├── venv/                 # Environnement virtuel Python
├── .env                  # Variables d'environnement (non versionné)
├── manage.py             # Script Django
└── requirements.txt      # Dépendances Python
```

## 🧪 Développement

### Commandes utiles

```bash
# Créer de nouvelles migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer les tests
python manage.py test

# Shell Django
python manage.py shell
```

### Workflow Git

```bash
# Créer une branche pour une nouvelle fonctionnalité
git checkout -b feature/nom-fonctionnalite

# Faire des commits réguliers
git add .
git commit -m "Description du changement"

# Pousser la branche
git push origin feature/nom-fonctionnalite

# Merger dans main après validation
git checkout main
git merge feature/nom-fonctionnalite
git push origin main
```

## 📊 État d'avancement

- [x] Setup projet Django
- [x] Configuration VS Code
- [x] Structure des applications
- [x] Page d'accueil
- [x] Interface admin
- [ ] Modèles de données Blog
- [ ] Modèles de données Events
- [ ] Modèles de données Members
- [ ] Intégration Tailwind CSS
- [ ] Migration contenu WordPress
- [ ] Widget météo
- [ ] Système d'inscription événements
- [ ] Tests unitaires
- [ ] Déploiement

## 👥 Contribution

Projet personnel - Alexandre Lousser

## 📝 Licence

Projet privé - Tous droits réservés - AMCD57

## 📧 Contact

Pour toute question : contact@amcd57.fr (à venir)

---

**🛩️ AMCD57 - Passion Aéromodélisme depuis [année de création]**
