# 🛩️ AMCD57 - Site Web du Club d'Aéromodélisme

Site web moderne du club d'aéromodélisme AMCD57 de Jarny (Grand Est, France).

Migration complète d'un site WordPress vers une stack Django moderne pour obtenir un contrôle total, de meilleures performances et une meilleure évolutivité.

## 📋 Fonctionnalités

### Phase 1 - Site de base (En cours de développement)

#### ✅ Complété

- **Pages statiques** : Structure de base (Accueil, Contact, À propos)
- **Blog complet** :
  - ✅ Modèle Article avec statut brouillon/publié
  - ✅ Modèle Catégorie (Club, Technique, Convention, Divers)
  - ✅ Modèle Tag pour mots-clés
  - ✅ Système de commentaires avec modération
  - ✅ Images à la une
  - ✅ Auteur visible
  - ✅ Compteur de vues
  - ✅ SEO (meta description)
  - ✅ Interface admin complète
- **Système d'événements complet** :
  - ✅ Modèle TypeEvenement (Réunion, Sortie, Vol)
  - ✅ Modèle Lieu avec coordonnées GPS
  - ✅ Modèle Evenement avec gestion avancée
  - ✅ Système d'inscription avec places limitées
  - ✅ Gestion des dates limites
  - ✅ Statuts (Planifié, Confirmé, Annulé, Terminé)
  - ✅ Suivi de présence
  - ✅ Accompagnants
  - ✅ Interface admin avec badges colorés

#### 🚧 En développement

- **Espace membre** : Profils, fonctions bureau, types de membres
- **Widget météo** : Conditions de vol temps réel (Jarny, France)
- **Liens web** : Annuaire organisé par catégories
- **Templates et vues** : Affichage frontend des contenus
- **Design** : Intégration Tailwind CSS

### Phase 2 - E-commerce (Futur)

- 🔮 Boutique en ligne (pièces, équipements, adhésions)
- 🔮 Gestion des cotisations
- 🔮 Paiement en ligne sécurisé (Stripe/PayPal)

## 🛠️ Stack Technique

### Backend

- **Django 5.0** - Framework web Python
- **django-allauth 0.57.0** - Système d'authentification (préparé)
- **Pillow** - Gestion des images
- **python-decouple** - Variables d'environnement
- **PostgreSQL** (production) / **SQLite** (développement)

### Frontend (À venir)

- **Templates Django** - Système de templates
- **Tailwind CSS** - Framework CSS moderne
- **HTMX/Alpine.js** - Interactivité légère

### APIs

- **OpenWeatherMap** - Météo en temps réel (à venir)

## 🗂️ Structure de la Base de Données

### Application Blog

```
Categorie (Club, Technique, Convention, Divers)
    ↓ (1:N)
Article ←→ Tag (N:N)
    ↓ (1:N)
Commentaire
```

### Application Events

```
TypeEvenement (Réunion, Sortie, Vol)
    ↓ (1:N)
Evenement ←─ Lieu (N:1)
    ↓ (1:N)
Inscription ←─ User (N:1)
```

### Application Members (À venir)

```
User (Django)
    ↓ (1:1)
ProfilMembre
    ↓ (N:N)
FonctionBureau
```

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
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env
# Éditer .env avec tes variables (voir section Variables d'environnement)

# Appliquer les migrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver
```

Le site sera accessible sur : http://127.0.0.1:8000/  
L'admin Django sur : http://127.0.0.1:8000/admin/

### Variables d'environnement (.env)

```env
# Django
SECRET_KEY=your-secret-key-here-generate-one
DEBUG=True

# Base de données (optionnel, SQLite par défaut)
# DATABASE_URL=postgresql://user:password@localhost:5432/amcd57

# API Keys
OPENWEATHER_API_KEY=your-openweather-api-key-here

# Email (pour plus tard)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=your@email.com
# EMAIL_HOST_PASSWORD=your_password
# EMAIL_USE_TLS=True
```

**Générer une SECRET_KEY :**

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## 📁 Structure du Projet

```
amcd57-django/
├── .vscode/              # Configuration VS Code
├── amcd57_project/       # Configuration Django
│   ├── settings.py       # Paramètres du projet
│   ├── urls.py           # Routes principales
│   └── wsgi.py
├── core/                 # Pages statiques et contenu principal
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── blog/                 # Application Blog
│   ├── models.py         # Article, Categorie, Tag, Commentaire
│   ├── admin.py          # Configuration admin
│   ├── views.py
│   └── migrations/
├── events/               # Application Events
│   ├── models.py         # Evenement, Lieu, TypeEvenement, Inscription
│   ├── admin.py          # Configuration admin
│   ├── views.py
│   └── migrations/
├── members/              # Application Members (à venir)
├── weblinks/             # Application Weblinks (à venir)
├── templates/            # Templates HTML globaux
│   ├── base/
│   ├── core/
│   ├── blog/
│   └── events/
├── static/               # Fichiers statiques (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                # Uploads utilisateurs
│   ├── blog/
│   └── events/
├── venv/                 # Environnement virtuel Python (non versionné)
├── .env                  # Variables d'environnement (non versionné)
├── .env.example          # Template des variables
├── .gitignore
├── manage.py             # Script Django
├── requirements.txt      # Dépendances Python
└── README.md
```

## 🧪 Développement

### Commandes Django utiles

```bash
# Créer de nouvelles migrations après modification des modèles
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser pour l'admin
python manage.py createsuperuser

# Collecter les fichiers statiques (production)
python manage.py collectstatic

# Lancer les tests
python manage.py test

# Shell Django (console Python interactive)
python manage.py shell

# Voir le SQL généré par une migration
python manage.py sqlmigrate blog 0001
```

### Workflow Git

```bash
# Créer une branche pour une nouvelle fonctionnalité
git checkout -b feature/nom-fonctionnalite

# Faire des commits réguliers avec messages descriptifs
git add .
git commit -m "✨ Description du changement"

# Pousser la branche
git push origin feature/nom-fonctionnalite

# Merger dans main après validation
git checkout main
git merge feature/nom-fonctionnalite
git push origin main
```

### Conventions de commit

```
✨ :sparkles: Nouvelle fonctionnalité
🐛 :bug: Correction de bug
📝 :memo: Documentation
🎨 :art: Amélioration du code (style)
♻️ :recycle: Refactoring
🚀 :rocket: Déploiement
🔧 :wrench: Configuration
✅ :white_check_mark: Tests
🔥 :fire: Suppression de code/fichiers
💄 :lipstick: Mise à jour UI/style
```

## 📊 État d'avancement

### Setup et Infrastructure

- [x] Setup projet Django
- [x] Configuration VS Code
- [x] Structure des 5 applications (core, blog, events, members, weblinks)
- [x] Configuration Git et GitHub
- [x] Variables d'environnement
- [x] Admin Django opérationnel

### Modèles de données

- [x] **Blog** : Article, Categorie, Tag, Commentaire
- [x] **Events** : Evenement, Lieu, TypeEvenement, Inscription
- [ ] **Members** : ProfilMembre, FonctionBureau, TypeMembre
- [ ] **Weblinks** : Lien, CategorieLien
- [ ] **Core** : ContactMessage

### Templates et Vues

- [x] Page d'accueil de base
- [ ] Liste des articles
- [ ] Détail d'un article
- [ ] Système de commentaires (frontend)
- [ ] Calendrier des événements
- [ ] Détail d'un événement
- [ ] Formulaire d'inscription événement
- [ ] Profil membre
- [ ] Dashboard membre

### Design et Frontend

- [ ] Intégration Tailwind CSS
- [ ] Design responsive
- [ ] Navigation principale
- [ ] Footer
- [ ] Composants réutilisables

### Fonctionnalités avancées

- [ ] Widget météo temps réel
- [ ] Recherche globale
- [ ] Filtres événements/articles
- [ ] Pagination
- [ ] Système de notifications
- [ ] Export calendrier (iCal)

### Migration WordPress

- [ ] Export contenu WordPress
- [ ] Script de migration des articles
- [ ] Migration des images
- [ ] Migration des événements
- [ ] Redirection URLs

### Tests et Qualité

- [ ] Tests unitaires modèles
- [ ] Tests vues
- [ ] Tests admin
- [ ] Documentation code
- [ ] Tests de performance

### Déploiement

- [ ] Choix hébergement
- [ ] Configuration PostgreSQL
- [ ] Configuration serveur web
- [ ] Certificat SSL
- [ ] Nom de domaine
- [ ] Monitoring

## 🎓 Technologies et Concepts Django utilisés

### Modèles

- ✅ ForeignKey (relations 1-N)
- ✅ ManyToManyField (relations N-N)
- ✅ OneToOneField (relations 1-1)
- ✅ Choices (listes déroulantes)
- ✅ Propriétés (@property)
- ✅ Méthodes personnalisées
- ✅ Validation (clean())
- ✅ Signaux (save override)
- ✅ Indexes pour performance
- ✅ Meta options (ordering, verbose_name)

### Admin Django

- ✅ ModelAdmin personnalisé
- ✅ Inline admin (TabularInline)
- ✅ Filtres (list_filter)
- ✅ Recherche (search_fields)
- ✅ Actions personnalisées
- ✅ Fieldsets
- ✅ Readonly fields
- ✅ Prepopulated fields
- ✅ Date hierarchy
- ✅ Custom display methods

## 👥 Contribution

Projet personnel - Alexandre Lousser

## 📝 Licence

Projet privé - Tous droits réservés - AMCD57

## 📧 Contact

Site actuel : [À venir]  
Email : contact@amcd57.fr (à venir)

---

**🛩️ AMCD57 - La passion de l'aéromodélisme depuis [année de création]**

_Projet en cours de développement - Dernière mise à jour : Octobre 2025_
