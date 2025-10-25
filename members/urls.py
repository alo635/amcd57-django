"""
URLs pour l'application Members AMCD57
"""

from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # Trombinoscope - Liste de tous les membres
    path('', views.trombinoscope, name='trombinoscope'),

    # Profil membre public
    path('profil/<int:pk>/', views.profil_detail, name='profil_detail'),

    # Page bureau du club
    path('bureau/', views.bureau, name='bureau'),

    # Dashboard membre (espace personnel)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Modification du profil
    path('profil/modifier/', views.profil_modifier, name='profil_modifier'),
]
