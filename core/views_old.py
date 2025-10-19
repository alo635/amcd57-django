from django.shortcuts import render
from django.views.generic import TemplateView


def home(request):
    """
    Page d'accueil du site AMCD57
    
    Args:
        request: La requête HTTP Django
        
    Returns:
        HttpResponse: La page d'accueil rendue
    """
    context = {
        'title': 'Accueil',
        'club_name': 'AMCD57',
        'slogan': 'Club d\'Aéromodélisme de Jarny',
    }
    return render(request, 'core/home.html', context)


def contact(request):
    """Page de contact"""
    context = {
        'title': 'Contact',
    }
    return render(request, 'core/contact.html', context)


def about(request):
    """Page À propos"""
    context = {
        'title': 'Qui sommes-nous ?',
    }
    return render(request, 'core/about.html', context)



