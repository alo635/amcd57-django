"""
URLs de l'application Core
Gère les routes des pages statiques
"""

from django.urls import path
from django.views.generic import TemplateView
from . import views

# Namespace pour éviter les conflits de noms d'URLs
app_name = 'core'

urlpatterns = [
    # Page d'accueil : http://127.0.0.1:8000/
    path('', views.home, name='home'),
    path('api/weather/', views.weather_widget, name='weather_api'),

    # Page contact : http://127.0.0.1:8000/contact/
    path('contact/', views.contact, name='contact'),

    path('a-propos/', views.about, name='about'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
    path('politique-confidentialite/', views.politique_confidentialite, name='politique_confidentialite'),
    path('cgu/', views.cgu, name='cgu'),

    # SEO - robots.txt
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]