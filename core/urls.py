"""
URLs de l'application Core
Gère les routes des pages statiques
"""

from django.urls import path
from . import views

# Namespace pour éviter les conflits de noms d'URLs
app_name = 'core'

urlpatterns = [
    # Page d'accueil : http://127.0.0.1:8000/
    path('', views.home, name='home'),
    
    # Page contact : http://127.0.0.1:8000/contact/
    # path('contact/', views.contact, name='contact'),
    
    # Page à propos : http://127.0.0.1:8000/qui-sommes-nous/
    # path('qui-sommes-nous/', views.about, name='about'),
]