"""
Vues pour l'application Events AMCD57
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta
from .models import Evenement, TypeEvenement, Lieu, Inscription


# ============================================
# LISTE DES ÉVÉNEMENTS
# ============================================

def evenement_list(request):
    """
    Affiche la liste des événements à venir
    URL : /evenements/
    """
    # Récupère les événements futurs et confirmés/planifiés
    now = timezone.now()
    evenements = Evenement.objects.filter(
        date_debut__gte=now,
        statut__in=['planifie', 'confirme']
    ).order_by('date_debut')
    
    # Filtrage par type d'événement
    type_slug = request.GET.get('type')
    type_obj = None  # ← AJOUT
    
    if type_slug:
        evenements = evenements.filter(type_evenement__slug=type_slug)
        try:
            type_obj = TypeEvenement.objects.get(slug=type_slug, actif=True)  # ← AJOUT
        except TypeEvenement.DoesNotExist:
            pass
    
    # Tous les types d'événements pour le filtre
    types_evenements = TypeEvenement.objects.filter(actif=True)
    
    # Événements à la une (featured ou prochains)
    evenements_featured = evenements.filter(
        date_debut__gte=now,
        date_debut__lte=now + timedelta(days=30)
    )[:3]
    
    context = {
        'evenements': evenements,
        'types_evenements': types_evenements,
        'evenements_featured': evenements_featured,
        'type_selectionne': type_slug,
        'type_obj': type_obj,  # ← AJOUT : objet TypeEvenement complet
    }
    
    return render(request, 'events/evenement_list.html', context)


# ============================================
# ÉVÉNEMENTS PASSÉS
# ============================================

def evenement_passes(request):
    """
    Affiche les événements passés
    URL : /evenements/passes/
    """
    now = timezone.now()
    evenements = Evenement.objects.filter(
        date_fin__lt=now
    ).order_by('-date_debut')[:20]  # Limité aux 20 derniers
    
    context = {
        'evenements': evenements,
    }
    
    return render(request, 'events/evenement_passes.html', context)


# ============================================
# CALENDRIER
# ============================================

def evenement_calendrier(request):
    """
    Affiche le calendrier des événements
    URL : /evenements/calendrier/
    """
    from calendar import monthrange, Calendar
    
    # Récupère le mois/année depuis les paramètres GET ou utilise le mois actuel
    now = timezone.now()
    
    try:
        annee = int(request.GET.get('annee', now.year))
        mois = int(request.GET.get('mois', now.month))
    except ValueError:
        annee = now.year
        mois = now.month
    
    # Calculer le premier et dernier jour du mois
    premier_jour = datetime(annee, mois, 1, tzinfo=timezone.get_current_timezone())
    dernier_jour_num = monthrange(annee, mois)[1]
    dernier_jour = datetime(annee, mois, dernier_jour_num, 23, 59, 59, tzinfo=timezone.get_current_timezone())
    
    # Récupère les événements du mois
    evenements = Evenement.objects.filter(
        Q(date_debut__gte=premier_jour, date_debut__lte=dernier_jour) |
        Q(date_fin__gte=premier_jour, date_fin__lte=dernier_jour) |
        Q(date_debut__lte=premier_jour, date_fin__gte=dernier_jour)
    ).exclude(statut='annule').order_by('date_debut')
    
    # Génération de la grille du calendrier
    cal = Calendar(firstweekday=0)  # Lundi = 0
    calendrier_jours = []
    
    for semaine in cal.monthdayscalendar(annee, mois):
        semaine_jours = []
        for jour_num in semaine:
            if jour_num == 0:
                # Jour d'un autre mois (vide)
                semaine_jours.append({
                    'numero': '',
                    'du_mois': False,
                    'est_aujourdhui': False
                })
            else:
                jour_date = datetime(annee, mois, jour_num, tzinfo=timezone.get_current_timezone()).date()
                semaine_jours.append({
                    'numero': jour_num,
                    'du_mois': True,
                    'est_aujourdhui': jour_date == now.date()
                })
        calendrier_jours.append(semaine_jours)
    
    # Mois précédent et suivant pour navigation
    if mois == 1:
        mois_precedent = 12
        annee_precedente = annee - 1
    else:
        mois_precedent = mois - 1
        annee_precedente = annee
    
    if mois == 12:
        mois_suivant = 1
        annee_suivante = annee + 1
    else:
        mois_suivant = mois + 1
        annee_suivante = annee
    
    context = {
        'evenements': evenements,
        'mois': mois,
        'annee': annee,
        'mois_nom': premier_jour.strftime('%B'),
        'mois_precedent': mois_precedent,
        'annee_precedente': annee_precedente,
        'mois_suivant': mois_suivant,
        'annee_suivante': annee_suivante,
        'calendrier_jours': calendrier_jours,
    }
    
    return render(request, 'events/evenement_calendrier.html', context)

# ============================================
# DÉTAIL D'UN ÉVÉNEMENT
# ============================================

def evenement_detail(request, slug):
    """
    Affiche le détail d'un événement
    URL : /evenements/<slug>/
    """
    evenement = get_object_or_404(Evenement, slug=slug)
    
    # Incrémente le compteur de vues
    evenement.incrementer_vues()
    
    # Vérifie si l'utilisateur est inscrit
    est_inscrit = False
    inscription = None
    if request.user.is_authenticated:
        try:
            inscription = Inscription.objects.get(
                evenement=evenement,
                participant=request.user
            )
            est_inscrit = True
        except Inscription.DoesNotExist:
            pass
    
    # Liste des inscrits (si l'événement le permet)
    inscrits = evenement.inscriptions.filter(
        statut='confirme'
    ).select_related('participant').order_by('date_inscription')
    
    context = {
        'evenement': evenement,
        'est_inscrit': est_inscrit,
        'inscription': inscription,
        'inscrits': inscrits,
    }
    
    return render(request, 'events/evenement_detail.html', context)


# ============================================
# INSCRIPTION À UN ÉVÉNEMENT
# ============================================

@login_required
def evenement_inscription(request, slug):
    """
    Inscription à un événement
    URL : /evenements/<slug>/inscription/
    """
    evenement = get_object_or_404(Evenement, slug=slug)
    
    # Vérifie que les inscriptions sont ouvertes
    if not evenement.inscriptions_ouvertes:
        messages.error(request, "Les inscriptions sont fermées pour cet événement.")
        return redirect('events:evenement_detail', slug=slug)
    
    # Vérifie que l'utilisateur n'est pas déjà inscrit
    if Inscription.objects.filter(evenement=evenement, participant=request.user).exists():
        messages.warning(request, "Vous êtes déjà inscrit à cet événement.")
        return redirect('events:evenement_detail', slug=slug)
    
    if request.method == 'POST':
        # Récupère le nombre d'accompagnants
        try:
            nombre_accompagnants = int(request.POST.get('nombre_accompagnants', 0))
        except ValueError:
            nombre_accompagnants = 0
        
        commentaire = request.POST.get('commentaire', '')
        
        # Crée l'inscription
        inscription = Inscription.objects.create(
            evenement=evenement,
            participant=request.user,
            nombre_accompagnants=nombre_accompagnants,
            commentaire=commentaire,
            statut='confirme'  # Confirmation automatique (peut être modifié pour validation manuelle)
        )
        
        messages.success(
            request,
            f"Votre inscription à l'événement '{evenement.titre}' a été confirmée !"
        )
        return redirect('events:mes_inscriptions')
    
    context = {
        'evenement': evenement,
    }
    
    return render(request, 'events/evenement_inscription.html', context)


# ============================================
# DÉSINSCRIPTION
# ============================================

@login_required
def evenement_desinscription(request, slug):
    """
    Désinscription d'un événement
    URL : /evenements/<slug>/desinscription/
    """
    evenement = get_object_or_404(Evenement, slug=slug)
    
    try:
        inscription = Inscription.objects.get(
            evenement=evenement,
            participant=request.user
        )
        inscription.delete()
        messages.success(request, f"Vous êtes désinscrit de l'événement '{evenement.titre}'.")
    except Inscription.DoesNotExist:
        messages.error(request, "Vous n'êtes pas inscrit à cet événement.")
    
    return redirect('events:evenement_detail', slug=slug)


# ============================================
# MES INSCRIPTIONS
# ============================================

@login_required
def mes_inscriptions(request):
    """
    Affiche les inscriptions de l'utilisateur connecté
    URL : /evenements/mes-inscriptions/
    """
    now = timezone.now()
    
    # Inscriptions aux événements à venir
    inscriptions_a_venir = Inscription.objects.filter(
        participant=request.user,
        evenement__date_debut__gte=now
    ).select_related('evenement', 'evenement__lieu', 'evenement__type_evenement').order_by('evenement__date_debut')
    
    # Inscriptions aux événements passés
    inscriptions_passees = Inscription.objects.filter(
        participant=request.user,
        evenement__date_fin__lt=now
    ).select_related('evenement').order_by('-evenement__date_debut')[:10]
    
    context = {
        'inscriptions_a_venir': inscriptions_a_venir,
        'inscriptions_passees': inscriptions_passees,
    }
    
    return render(request, 'events/mes_inscriptions.html', context)


# ============================================
# ÉVÉNEMENTS PAR TYPE
# ============================================

def evenements_par_type(request, slug):
    """
    Affiche les événements d'un type spécifique
    URL : /evenements/type/<slug>/
    """
    type_evenement = get_object_or_404(TypeEvenement, slug=slug, actif=True)
    
    now = timezone.now()
    evenements = Evenement.objects.filter(
        type_evenement=type_evenement,
        date_debut__gte=now,
        statut__in=['planifie', 'confirme']
    ).order_by('date_debut')
    
    context = {
        'type_evenement': type_evenement,
        'evenements': evenements,
    }
    
    return render(request, 'events/evenements_par_type.html', context)