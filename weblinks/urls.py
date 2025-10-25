"""
URLs pour l'application Weblinks AMCD57
"""

from django.urls import path
from . import views

app_name = 'weblinks'

urlpatterns = [
    # Annuaire de liens - Liste principale
    path('', views.annuaire, name='annuaire'),

    # Liens par catégorie
    path('categorie/<slug:slug>/', views.categorie_detail, name='categorie_detail'),

    # Redirection vers un lien externe avec compteur de clics
    path('redirect/<int:pk>/', views.lien_redirect, name='lien_redirect'),
]
