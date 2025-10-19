"""
Vues pour l'application Core AMCD57
"""

from django.shortcuts import render
from django.utils import timezone
from blog.models import Article
from events.models import Evenement
from members.models import ProfilMembre


def home(request):
    """
    Page d'accueil du site
    URL : /
    """
    now = timezone.now()
    
    # Récupère les 3 derniers articles publiés
    articles_recents = Article.objects.filter(
        statut='publie',
        date_publication__lte=now
    ).select_related('categorie', 'auteur').order_by('-date_publication')[:3]
    
    # Récupère les 3 prochains événements
    evenements_a_venir = Evenement.objects.filter(
        date_debut__gte=now,
        statut__in=['planifie', 'confirme']
    ).select_related('type_evenement', 'lieu').order_by('date_debut')[:3]
    
    # Statistiques du club
    stats = {
        'nombre_membres': ProfilMembre.objects.filter(
            user__is_active=True,
            cotisation_a_jour=True
        ).count(),
        'nombre_evenements': Evenement.objects.filter(
            date_debut__gte=now,
            statut__in=['planifie', 'confirme']
        ).count(),
        'nombre_articles': Article.objects.filter(statut='publie').count(),
    }
    
    context = {
        'articles_recents': articles_recents,
        'evenements_a_venir': evenements_a_venir,
        'stats': stats,
    }
    
    return render(request, 'core/home.html', context)