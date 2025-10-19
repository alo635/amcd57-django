"""
URLs de l'application Events
"""

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Liste des événements : /evenements/
    path('', views.evenement_list, name='evenement_list'),
    
    # Événements passés : /evenements/passes/
    path('passes/', views.evenement_passes, name='evenement_passes'),
    
    # Calendrier : /evenements/calendrier/
    path('calendrier/', views.evenement_calendrier, name='evenement_calendrier'),
    
    # Mes inscriptions : /evenements/mes-inscriptions/
    path('mes-inscriptions/', views.mes_inscriptions, name='mes_inscriptions'),
    
    # Type d'événement : /evenements/type/reunion/
    path('type/<slug:slug>/', views.evenements_par_type, name='evenements_par_type'),
    
    # Inscription : /evenements/<slug>/inscription/
    path('<slug:slug>/inscription/', views.evenement_inscription, name='evenement_inscription'),
    
    # Désinscription : /evenements/<slug>/desinscription/
    path('<slug:slug>/desinscription/', views.evenement_desinscription, name='evenement_desinscription'),
    
    # Détail événement : /evenements/<slug>/
    path('<slug:slug>/', views.evenement_detail, name='evenement_detail'),
]