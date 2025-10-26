"""
Configuration Django pour AMCD57
Ce fichier contient tous les paramètres du projet

Documentation Django : https://docs.djangoproject.com/fr/5.0/
"""

from pathlib import Path
from decouple import config
import os

# Chemin de base du projet
# BASE_DIR pointe vers la racine du projet (là où se trouve manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-CHANGE-THIS-IN-PRODUCTION')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
# IMPORTANT : L'ordre est crucial !
# Les apps Django de base doivent être chargées AVANT allauth
INSTALLED_APPS = [
    # Apps Django de base (doivent être en premier)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Requis pour allauth
    'django.contrib.sitemaps',  # Pour le SEO (sitemap.xml)

    # Applications tierces
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Nos applications
    'core',
    'blog',
    'events',
    'members',
    'weblinks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Pour allauth
]

ROOT_URLCONF = 'amcd57_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Dossier templates global
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'amcd57_project.wsgi.application'

# Database - SQLite pour le développement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'  # Français
TIME_ZONE = 'Europe/Paris'  # Fuseau horaire France
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Fichiers statiques globaux
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Pour la production

# Media files (uploads utilisateurs)
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = config('MEDIA_ROOT', default=str(BASE_DIR / 'media'))

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration django-allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Configuration de l'authentification
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Connexion par email
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False  # Pas de username obligatoire
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Vérification email optionnelle en dev
LOGIN_REDIRECT_URL = '/membres/dashboard/'  # Après connexion
LOGOUT_REDIRECT_URL = '/'  # Après déconnexion

# API Keys (à configurer plus tard)
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY', default='')

# Cache (pour stocker temporairement les données météo)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}