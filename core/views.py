"""
Vues pour l'application Core AMCD57
"""

from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from blog.models import Article
from events.models import Evenement
from members.models import ProfilMembre
from django.core.cache import cache
from .services.weather import WeatherService
from django.contrib import messages
from .models import ContactMessage


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

def contact(request):
    """
    Page de contact avec formulaire
    URL : /contact/
    """
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        sujet = request.POST.get('sujet', '')
        message_text = request.POST.get('message', '').strip()
        
        # Validation simple
        if not nom or not email or not message_text:
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return redirect('core:contact')
        
        # Récupération de l'IP (optionnel)
        ip_address = request.META.get('REMOTE_ADDR', '')
        
        # Création du message de contact
        try:
            contact_message = ContactMessage.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message_text,
                ip_address=ip_address,
                statut='nouveau',
                lu=False
            )
            
            # TODO: Envoyer un email de notification au club
            # send_mail(
            #     subject=f"[AMCD57] Nouveau message de contact - {sujet}",
            #     message=f"De: {nom} ({email})\n\n{message_text}",
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=['contact@amcd57.fr'],
            # )
            
            messages.success(
                request,
                "✅ Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais."
            )
            return redirect('core:home')
            
        except Exception as e:
            messages.error(
                request,
                "❌ Une erreur est survenue lors de l'envoi de votre message. Veuillez réessayer."
            )
            return redirect('core:contact')
    
    # GET - Affichage du formulaire
    context = {
        'sujets': ContactMessage.SUJET_CHOICES,
    }
    
    return render(request, 'core/contact.html', context)