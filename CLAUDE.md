# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AMCD57 is an aeromodeling club website built with Django 5.0. This is a complete migration from WordPress to a modern Django stack, providing better performance, full control, and scalability. The project is French-language focused and serves the AMCD57 aeromodeling club in Delme, Grand Est, France.

**Current Status**: 98% complete - core functionality fully implemented, ready for WordPress content migration.

## Technology Stack

- **Backend**: Django 5.0 (Python 3.13+)
- **Frontend**: Tailwind CSS (via CDN), Django templates
- **Database**: SQLite (development), PostgreSQL (production planned)
- **Authentication**: django-allauth 0.57.0 (email-based)
- **APIs**: OpenWeatherMap (weather widget)
- **Media**: Pillow for image handling

## Architecture

### Application Structure

The project follows Django's app-based architecture with 5 main applications:

1. **core** - Static pages, homepage, contact form, weather widget
2. **blog** - Articles, categories, tags, comments with moderation
3. **events** - Events management with registration system, calendar, venues
4. **members** - Extended user profiles, club membership, bureau functions
5. **weblinks** - Links directory (models complete, templates pending)

### Key Design Patterns

**Model Relationships**:
- The project extensively uses Django's relationship fields (ForeignKey, ManyToMany, OneToOne)
- All models use slug-based URLs for SEO
- Auto-generation of slugs with uniqueness checking in save() methods
- @property decorators for calculated fields (age, places_restantes, nombre_articles, etc.)

**Authentication Flow**:
- Login redirects to `/membres/dashboard/`
- Logout redirects to `/`
- Email-based authentication (no username required)
- User model extended via OneToOne relationship with ProfilMembre

**Permission System**:
- Members have TypeMembre defining access rights (peut_voter, acces_terrain, acces_espace_membre)
- Bureau members have FonctionBureau with fonction_active boolean
- Check permissions with `user.profil.est_membre_bureau` property
- Admin menu visible only to bureau members

**Template Inheritance**:
- Base template: `templates/base/base.html` (includes Tailwind CSS via CDN)
- All templates extend base and override blocks (title, content, extra_css, extra_js)
- Shared components in includes (e.g., weather widget)

### Data Flow

**Event Registration System** (complex workflow):
1. User views event detail → checks `evenement.inscriptions_ouvertes`
2. Validates: date_limite_inscription, places_restantes, est_passe
3. Creates Inscription with statut='en_attente'
4. Admin confirms → statut='confirme'
5. After event → mark present=True for attendance tracking

**Blog Comment Moderation**:
1. User/visitor submits comment → approuve=False by default
2. Admin approves in admin interface → approuve=True
3. Only approved comments display in article_detail template
4. Supports threaded replies via parent ForeignKey

**Weather Widget Caching**:
- Service class in `core/services/weather.py`
- 30-minute cache for current weather
- 1-hour cache for forecasts
- OpenWeatherMap API for Delme coordinates (49.1586, 5.8808)

## Common Development Commands

### Initial Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with SECRET_KEY and OPENWEATHER_API_KEY

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Database Migrations
```bash
# After modifying models
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View SQL for a migration
python manage.py sqlmigrate blog 0001
```

### Testing & Development
```bash
# Run tests (when implemented)
python manage.py test

# Django shell for debugging
python manage.py shell

# Clear cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

### Production Preparation
```bash
# Collect static files
python manage.py collectstatic

# Check for deployment issues
python manage.py check --deploy
```

## Important Conventions

### Model Design
- Always include slug field with auto-generation in save()
- Use timezone.now for default dates (never datetime.now)
- Add indexes for frequently queried fields (date, statut, foreign keys)
- Include verbose_name and help_text for admin clarity
- Implement get_absolute_url() using reverse() for URL generation
- Use @property for computed fields, not storing redundant data

### Admin Configuration
- Use @admin.register() decorator (cleaner than admin.site.register)
- Configure list_display, list_filter, search_fields for usability
- Use prepopulated_fields for slugs
- Add fieldsets to organize forms
- Implement custom actions for bulk operations (e.g., approve comments)
- Use InlineModelAdmin for related objects (e.g., comments in articles)
- Set readonly_fields for auto-generated or calculated fields

### Views & Templates
- Use Function-Based Views (FBV) - project doesn't use CBVs
- Always use get_object_or_404 for single object retrieval
- Implement pagination with Paginator for list views
- Use Django messages framework for user feedback
- Increment view counters with update_fields to avoid race conditions:
  ```python
  article.vues += 1
  article.save(update_fields=['vues'])
  ```

### URL Routing
- Main URLs in `amcd57_project/urls.py` include app URLs
- App URLs use app_name for namespacing:
  ```python
  # blog/urls.py
  app_name = 'blog'
  ```
- Reference URLs in templates: `{% url 'blog:article_detail' slug=article.slug %}`
- Use slug-based URLs, not PKs, for SEO

### Template Tags & Filters
- Custom template tags in app `templatetags/` directory
- Example: `events/templatetags/event_filters.py` for calendar helpers
- Load custom tags: `{% load event_filters %}`
- Use Django's built-in filters: date, truncatewords, linebreaks, pluralize

## Application-Specific Notes

### Blog App
- Articles have STATUT_CHOICES: 'brouillon' or 'publie'
- Auto-generate extrait from content if blank (first 150 chars)
- Set date_publication when publishing (statut changes to 'publie')
- Comments require approval (approuve=False by default)
- Images stored in `media/blog/articles/%Y/%m/` for organization

### Events App
- TypeEvenement has couleur (hex) and icone (emoji) for visual categorization
- Evenement validation in clean() method (date_fin > date_debut, etc.)
- Complex inscription logic - always check inscriptions_ouvertes property
- places_restantes calculated dynamically (nombre_places - nombre_inscrits)
- Custom template tags for calendar generation
- Four STATUT_CHOICES: planifie, confirme, annule, termine

### Members App
- ProfilMembre extends User via OneToOneField (DO NOT modify User directly)
- Signal for auto-creating profiles is commented out - create manually via admin
- TypeMembre defines permissions (peut_voter, acces_terrain, acces_espace_membre)
- FonctionBureau tracks bureau positions - check fonction_active for current holders
- Calculate age and anciennete_annees via @property (not stored fields)
- Phone validation using RegexValidator
- License renewal logic in renouveler_cotisation() method

### Core App
- Weather service uses class-based design in services/weather.py
- Contact form saves to ContactMessage model with workflow states
- Static pages (about, legal, privacy, terms) in dedicated templates
- Homepage pulls latest articles and upcoming events dynamically

## Environment Variables

Required in `.env` file:

```env
SECRET_KEY=<generate-with-django>
DEBUG=True
OPENWEATHER_API_KEY=<your-api-key>

# Production only:
# DATABASE_URL=postgresql://user:pass@localhost/dbname
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=email@example.com
# EMAIL_HOST_PASSWORD=password
# EMAIL_USE_TLS=True
```

Generate SECRET_KEY:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Database Schema Notes

**Key Relationships to Remember**:
- Article → Categorie (ForeignKey with PROTECT - cannot delete category with articles)
- Article ↔ Tag (ManyToMany)
- Commentaire → Article (ForeignKey with CASCADE)
- Commentaire → Commentaire (self-referential for replies)
- Evenement → TypeEvenement (ForeignKey with PROTECT)
- Evenement → Lieu (ForeignKey with SET_NULL - event survives if venue deleted)
- Inscription unique_together on (evenement, participant) - prevents duplicate signups
- ProfilMembre → User (OneToOne with CASCADE)
- ProfilMembre → TypeMembre (ForeignKey with PROTECT)

**Indexes for Performance**:
All major models have indexes on frequently queried fields:
- Article: date_publication, statut, slug
- Evenement: date_debut, statut, type_evenement
- Commentaire: (article, approuve) composite index
- Inscription: (evenement, statut) composite index

## Known Limitations & TODOs

1. **Members & Weblinks Templates**: Models complete but frontend templates not implemented
2. **WordPress Migration**: 15 articles + 62 images need migration script
3. **Mobile Menu**: Hamburger menu not yet implemented
4. **Testing**: No test suite yet - write tests before production
5. **Tailwind**: Currently via CDN - should build custom for production
6. **Email**: Email backend not configured (needed for allauth verification)

## Troubleshooting

**Migration Issues**:
- If migrations conflict, check for multiple migration files with same number
- Use `python manage.py migrate --fake` only if you know what you're doing
- Better: `python manage.py migrate app_name migration_name` for specific migrations

**Static Files Not Loading**:
- In development, ensure `DEBUG=True` and static middleware is active
- Check STATIC_URL and STATICFILES_DIRS in settings.py
- Run `python manage.py collectstatic` for production

**ProfilMembre Not Created**:
- Auto-creation signal is commented out
- Manually create ProfilMembre in admin for each User
- Or uncomment signal in members/models.py (lines 475-503)

**Weather Widget Not Working**:
- Verify OPENWEATHER_API_KEY in .env
- Check cache: `cache.delete('weather_current_jarny')`
- API has rate limits - cache helps avoid hitting them

## File Organization

```
amcd57-django/
├── amcd57_project/         # Django project settings
│   ├── settings.py         # All configuration (apps, middleware, DB, etc.)
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI entry point
├── core/                   # Static pages & homepage
│   ├── services/
│   │   └── weather.py      # Weather API service class
│   ├── models.py           # ContactMessage model
│   └── views.py            # FBVs for home, contact, about, legal pages
├── blog/                   # Blog application
│   ├── models.py           # Article, Categorie, Tag, Commentaire
│   ├── admin.py            # Admin config with inlines and actions
│   └── views.py            # List, detail, search, category, tag views
├── events/                 # Events management
│   ├── models.py           # Evenement, Lieu, TypeEvenement, Inscription
│   ├── templatetags/
│   │   └── event_filters.py # Custom template tags for calendar
│   └── views.py            # Event list, detail, calendar, registration
├── members/                # Member management
│   ├── models.py           # ProfilMembre, TypeMembre, FonctionBureau
│   └── admin.py            # Extended UserAdmin with inline profil
├── weblinks/               # Links directory (templates pending)
│   └── models.py           # Lien, CategorieLien
├── templates/              # Global templates
│   ├── base/
│   │   └── base.html       # Base template with Tailwind CSS
│   ├── core/               # 6 templates (home, contact, about, legal, etc.)
│   ├── blog/               # 5 templates (list, detail, search, etc.)
│   └── events/             # 6 templates (list, detail, calendar, etc.)
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploads (organized by app and date)
└── requirements.txt        # Python dependencies
```

## Admin Interface Access

- URL: http://127.0.0.1:8000/admin/
- Login with superuser credentials
- All models configured with rich admin interfaces
- Use bulk actions for efficiency (approve comments, renew memberships, etc.)
- Inline editing where logical (comments in articles, profil in user)

## Design Philosophy

This project prioritizes:
- **French language** throughout (models, admin, templates)
- **SEO-friendly URLs** (slug-based)
- **Performance** (caching, indexes, optimized queries)
- **User experience** (Tailwind CSS, responsive design, clear feedback messages)
- **Data integrity** (validation in clean(), PROTECT on critical FKs, unique_together)
- **Flexibility** (statut choices, TypeEvenement colors, permission system)

When adding features, maintain these principles and follow existing patterns for consistency.
