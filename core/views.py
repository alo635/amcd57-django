"""
Vues pour l'application Core AMCD57
"""

from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from blog.models import Article
from events.models import Evenement
from members.models import ProfilMembre
from django.core.cache import cache
from .services.weather import WeatherService


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
    # Vider le cache météo (temporaire pour debug)
    #cache.delete('weather_current_jarny')

    # Météo
    weather_service = WeatherService()
    current_weather = weather_service.get_current_weather()

    # ← AJOUT DE LOGS
    #print("=" * 50)
    #print("🌤️  DONNÉES MÉTÉO DANS LA VUE :")
    #print(f"Type : {type(current_weather)}")
    #print(f"Contenu : {current_weather}")
    #print("=" * 50)

    # Conditions de vol
    if current_weather.get('success'):
        current_weather['good_for_flying'] = weather_service.is_good_flying_conditions(current_weather)
        current_weather['wind_direction_text'] = weather_service.get_wind_direction_text(current_weather['wind_direction'])


    context = {
        'articles_recents': articles_recents,
        'evenements_a_venir': evenements_a_venir,
        'stats': stats,
        'weather': current_weather,
    }
    
    return render(request, 'core/home.html', context)

def weather_widget(request):
    """
    API pour le widget météo
    Retourne les données météo en JSON
    URL : /api/weather/
    """
    weather_service = WeatherService()
    current_weather = weather_service.get_current_weather()
    forecast = weather_service.get_forecast(days=5)
    
    if current_weather.get('success'):
        current_weather['good_for_flying'] = weather_service.is_good_flying_conditions(current_weather)
        current_weather['wind_direction_text'] = weather_service.get_wind_direction_text(current_weather['wind_direction'])
    
    return JsonResponse({
        'current': current_weather,
        'forecast': forecast
    })