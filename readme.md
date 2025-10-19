## 🔑 Fonctionnalités clés implémentées

### Blog (100% ✅)
- Système de brouillon/publication
- Auto-génération des slugs
- Images à la une organisées par date
- Compteur de vues avec incrémentation automatique
- Système de commentaires avec modération
- Support réponses aux commentaires (threading)
- SEO (meta descriptions)
- Filtres par catégorie, tag, statut, date
- **Frontend complet** :
  - Liste paginée des articles (9 par page)
  - Page détail avec commentaires fonctionnels
  - Filtrage par catégorie avec compteurs
  - Filtrage par tag
  - Recherche fulltext (titre, contenu, extrait)
  - Articles similaires (même catégorie)
  - Sidebar avec articles récents et tags
  - Formulaire de commentaires (visiteurs et membres)
  - Messages de confirmation Django
  - Navigation fil d'Ariane
  - Design responsive inline CSS (en attente Tailwind)

### Events
- Types d'événements personnalisables avec couleurs
- Gestion de lieux avec coordonnées GPS
- Inscriptions avec places limitées
- Dates limites d'inscription
- Statuts multiples (Planifié, Confirmé, Annulé, Terminé)
- Suivi de présence après événement
- Gestion des accompagnants
- Calcul automatique des places restantes
- Vérification si événement complet
- Événements publics ou membres uniquement

### Members
- Extension complète du modèle User Django
- Types de membres avec droits différenciés
- Fonctions bureau avec email de contact
- Profil intégré dans l'admin User
- Informations personnelles et adresse
- Expérience et spécialités aéromodélisme
- Licence UFOLEP avec date de validité
- Assurance RC
- Gestion cotisations avec dates
- Calcul automatique âge et ancienneté
- Réseaux sociaux (YouTube, Facebook, Instagram)
- Préférences (newsletter, notifications)
- Actions en masse (renouvellement cotisations)
- Notes administratives privées

### Weblinks
- Catégories personnalisables avec icônes
- Liens organisés par catégorie
- Compteur de clics par lien
- Tags pour recherche et filtrage
- Liens "mis en avant" (featured)
- Extraction automatique du domaine
- Logo/capture d'écran du site
- Ouverture nouvel onglet configurable
- Statistiques de clics
- Notes administratives

### Core - Contact
- Formulaire de contact avec sujets prédéfinis
- Workflow complet (Nouveau → En cours → Traité → Archivé)
- Suivi lu/non lu
- Suivi répondu avec date
- Calcul âge du message
- Tracking IP
- Notes de réponse internes
- Recherche et filtres avancés
- Actions en masse (traiter, archiver)
- Badges colorés par statut et sujet# 🛩️ AMCD57 - Site Web du Club d'Aéromodélisme

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

### Application Blog (4 modèles) ✅
```
Categorie (Club, Technique, Convention, Divers)
    ↓ (1:N)
Article ←→ Tag (N:N)
    ↓ (1:N)
    ↓ User (auteur)
    ↓
Commentaire (avec réponses)
```

**Fonctionnalités** : Brouillon/Publié, Images, SEO, Compteur de vues, Modération commentaires, Auto-génération slugs

### Application Events (4 modèles) ✅
```
TypeEvenement (Réunion, Sortie, Vol) - avec couleurs
    ↓ (1:N)
Evenement ←─ Lieu (N:1)
    ↓ (1:N)        ↑ (GPS, capacité)
    ↓ User (organisateur)
    ↓
Inscription ←─ User (participant)
    ↓ (accompagnants, présence)
```

**Fonctionnalités** : Places limitées, Dates limites, Statuts multiples, Présences, Accompagnants, Calcul places restantes

### Application Members (3 modèles) ✅
```
TypeMembre (Bureau, Actif) - avec droits
    ↓ (1:N)
ProfilMembre (1:1) ←→ User (Django)
    ↓ (N:1)
FonctionBureau (Président, Trésorier, etc.)
    ↑ (fonction_active boolean)
```

**Fonctionnalités** : Licence UFOLEP, Assurance RC, Cotisations, Droits/Permissions, Fonction bureau active, Calculs automatiques (âge, ancienneté), Réseaux sociaux

### Application Weblinks (2 modèles) ✅
```
CategorieLien (Officiels, Clubs, Techniques, Boutiques)
    ↓ (1:N)
Lien (URL, logo, tags, compteur clics)
    ↑ (featured, actif)
```

**Fonctionnalités** : Compteur de clics, Tags, Featured links, Extraction domaine, Ouverture nouvel onglet

### Application Core (1 modèle) ✅
```
ContactMessage (formulaire de contact)
    ↓ Sujet (Info, Adhésion, Événement, etc.)
    ↓ Statut (Nouveau, En cours, Traité, Archivé)
    ↓ Lu/Répondu tracking
```

**Fonctionnalités** : Choix sujets multiples, Statuts workflow, Suivi lu/répondu, Calcul âge message, IP tracking, Notes internes

---

### 📊 Statistiques de la base de données

**Total : 13 modèles créés**
- Relations ForeignKey (1-N) : 10
- Relations ManyToManyField (N-N) : 2
- Relations OneToOneField (1-1) : 1
- Champs avec Choices : 8
- Propriétés calculées (@property) : 25+
- Indexes pour performance : 15+

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
- [x] **Members** : ProfilMembre, FonctionBureau, TypeMembre
- [ ] **Weblinks** : Lien, CategorieLien
- [ ] **Core** : ContactMessage

### Templates et Vues (20% - En cours)

#### ✅ Blog (100% complété)
- [x] Liste des articles avec pagination (9/page)
- [x] Détail d'un article avec commentaires
- [x] Articles par catégorie
- [x] Articles par tag
- [x] Recherche fulltext dans les articles
- [x] Formulaire de commentaires (membres et visiteurs)
- [x] Articles similaires (même catégorie)
- [x] Sidebar (articles récents, tags populaires)
- [x] Compteur de vues automatique
- [x] 5 vues créées et fonctionnelles
- [x] 5 templates responsive

#### 🚧 Events (0% - Prochaine étape)
- [ ] Calendrier des événements
- [ ] Liste des événements
- [ ] Détail d'un événement
- [ ] Formulaire d'inscription événement
- [ ] Mes inscriptions
- [ ] Filtres par type d'événement

#### 🚧 Members (0%)
- [ ] Trombinoscope membres
- [ ] Profil membre public
- [ ] Page bureau du club
- [ ] Dashboard membre
- [ ] Modification profil

#### 🚧 Weblinks (0%)
- [ ] Annuaire de liens par catégories
- [ ] Redirection avec compteur de clics

#### 🚧 Core (0%)
- [ ] Formulaire de contact fonctionnel
- [ ] Pages statiques (À propos, etc.)
- [ ] Page d'accueil enrichie

### Design et Frontend (10%)
- [x] Templates de base avec CSS inline
- [x] Navigation principale
- [x] Messages Django (success/error)
- [x] Design responsive basique
- [ ] Intégration Tailwind CSS
- [ ] Composants réutilisables
- [ ] Footer complet
- [ ] Menu mobile hamburger

### Fonctionnalités avancées (0%)
- [ ] Widget météo temps réel (OpenWeatherMap)
- [ ] Recherche globale multi-applications
- [ ] Système de notifications
- [ ] Export calendrier (iCal)
- [ ] Partage réseaux sociaux
- [ ] Newsletter
- [ ] Sitemap XML
- [ ] RSS Feed

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
- ✅ Signaux (post_save - désactivé pour Members)
- ✅ Indexes pour performance
- ✅ Meta options (ordering, verbose_name, unique_together)
- ✅ Validators (RegexValidator pour téléphones)
- ✅ Calculs automatiques (âge, ancienneté, places restantes)

### Vues
- ✅ Function-Based Views (FBV)
- ✅ get_object_or_404
- ✅ Pagination (Paginator)
- ✅ Recherche avec Q objects
- ✅ Formulaires POST
- ✅ Messages Django (success/error)
- ✅ Context data pour templates
- ✅ Redirections

### Templates
- ✅ Template inheritance (extends)
- ✅ Template blocks
- ✅ Template tags (for, if, with)
- ✅ Template filters (date, truncatewords, linebreaks)
- ✅ URL reversing ({% url %})
- ✅ Static files ({% static %})
- ✅ CSRF protection ({% csrf_token %})
- ✅ Conditional rendering

### Admin Django
- ✅ ModelAdmin personnalisé
- ✅ Inline admin (TabularInline, StackedInline)
- ✅ Filtres (list_filter)
- ✅ Recherche (search_fields)
- ✅ Actions personnalisées (actions en masse)
- ✅ Fieldsets (organisation des champs)
- ✅ Readonly fields
- ✅ Prepopulated fields (slugs)
- ✅ Date hierarchy
- ✅ Custom display methods avec format_html
- ✅ List editable (modification rapide)
- ✅ Extension de UserAdmin

## 👥 Contribution

Projet personnel - Alexandre Lousser

## 📝 Licence

Projet privé - Tous droits réservés - AMCD57

## 📧 Contact

Site actuel : [À venir]  
Email : contact@amcd57.fr (à venir)

---

**🛩️ AMCD57 - La passion de l'aéromodélisme depuis [année de création]**

*Projet en cours de développement - Dernière mise à jour : Octobre 2025*

**🎉 Étape majeure franchie : 13/13 modèles créés (100%) !**  
**🚀 Prochaine étape : Création des vues et templates pour afficher le contenu**