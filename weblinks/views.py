"""
Vues pour l'application Weblinks AMCD57
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Lien, CategorieLien


# ============================================
# ANNUAIRE - Liste de tous les liens
# ============================================

def annuaire(request):
    """
    Affiche l'annuaire complet des liens organisés par catégories
    Filtres possibles : recherche par nom/description
    """
    # Récupérer toutes les catégories actives avec leurs liens actifs
    categories = CategorieLien.objects.filter(actif=True).prefetch_related('liens')

    # Recherche
    search = request.GET.get('search')
    liens_recherche = None

    if search:
        # Rechercher dans tous les liens actifs
        liens_recherche = Lien.objects.filter(
            Q(titre__icontains=search) |
            Q(description__icontains=search) |
            Q(tags__icontains=search),
            actif=True
        ).select_related('categorie').order_by('ordre', 'titre')

    # Récupérer les liens mis en avant (featured)
    liens_featured = Lien.objects.filter(
        actif=True,
        featured=True
    ).select_related('categorie').order_by('ordre')[:6]

    context = {
        'categories': categories,
        'liens_featured': liens_featured,
        'search': search,
        'liens_recherche': liens_recherche,
    }

    return render(request, 'weblinks/annuaire.html', context)


# ============================================
# CATÉGORIE DETAIL - Liens d'une catégorie
# ============================================

def categorie_detail(request, slug):
    """
    Affiche tous les liens d'une catégorie spécifique
    """
    categorie = get_object_or_404(CategorieLien, slug=slug, actif=True)

    # Récupérer les liens actifs de cette catégorie
    liens = categorie.liens_actifs  # Utilise la @property du modèle

    context = {
        'categorie': categorie,
        'liens': liens,
    }

    return render(request, 'weblinks/categorie_detail.html', context)


# ============================================
# REDIRECTION - Compteur de clics
# ============================================

def lien_redirect(request, pk):
    """
    Redirige vers le lien externe et incrémente le compteur de clics
    """
    lien = get_object_or_404(Lien, pk=pk, actif=True)

    # Incrémenter le compteur de clics
    lien.incrementer_clics()

    # Rediriger vers l'URL externe
    return redirect(lien.url)
