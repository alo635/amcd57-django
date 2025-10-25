"""
Vues pour l'application Members AMCD57
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import ProfilMembre, FonctionBureau, TypeMembre
from events.models import Inscription


# ============================================
# TROMBINOSCOPE - Liste des membres
# ============================================

def trombinoscope(request):
    """
    Affiche la liste de tous les membres avec leurs photos
    Filtres possibles : type de membre, recherche par nom
    """
    # Récupérer tous les profils de membres actifs
    profils = ProfilMembre.objects.filter(
        user__is_active=True
    ).select_related('user', 'type_membre', 'fonction_bureau')

    # Filtre par type de membre
    type_filtre = request.GET.get('type')
    if type_filtre:
        profils = profils.filter(type_membre__nom=type_filtre)

    # Recherche par nom
    search = request.GET.get('search')
    if search:
        profils = profils.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__username__icontains=search)
        )

    # Filtrer uniquement les profils publics (sauf si membre connecté)
    if not request.user.is_authenticated:
        profils = profils.filter(profil_public=True)

    # Ordre : Bureau en premier, puis par nom
    profils = profils.order_by('-fonction_active', 'user__last_name', 'user__first_name')

    # Récupérer tous les types de membres pour le filtre
    types_membres = TypeMembre.objects.filter(actif=True)

    context = {
        'profils': profils,
        'types_membres': types_membres,
        'type_filtre': type_filtre,
        'search': search,
        'total_membres': profils.count(),
    }

    return render(request, 'members/trombinoscope.html', context)


# ============================================
# PROFIL MEMBRE PUBLIC
# ============================================

def profil_detail(request, pk):
    """
    Affiche le profil public d'un membre
    """
    profil = get_object_or_404(ProfilMembre, pk=pk)

    # Vérifier si le profil est public ou si c'est le propriétaire ou membre connecté
    if not profil.profil_public and not request.user.is_authenticated:
        messages.warning(request, "Ce profil n'est pas public.")
        return redirect('members:trombinoscope')

    # Si c'est le propriétaire du profil, rediriger vers le dashboard
    if request.user.is_authenticated and profil.user == request.user:
        return redirect('members:dashboard')

    # Récupérer les inscriptions aux événements à venir du membre (si profil public)
    inscriptions_futures = None
    if profil.profil_public:
        inscriptions_futures = Inscription.objects.filter(
            participant=profil.user,
            statut='confirme',
            evenement__date_debut__gte=timezone.now()
        ).select_related('evenement').order_by('evenement__date_debut')[:5]

    context = {
        'profil': profil,
        'inscriptions_futures': inscriptions_futures,
    }

    return render(request, 'members/profil_detail.html', context)


# ============================================
# PAGE BUREAU DU CLUB
# ============================================

def bureau(request):
    """
    Affiche la page du bureau du club avec tous les membres actifs
    """
    # Récupérer toutes les fonctions bureau actives
    fonctions = FonctionBureau.objects.filter(actif=True).order_by('ordre')

    # Pour chaque fonction, récupérer le membre actuel
    bureau_membres = []
    for fonction in fonctions:
        membre = fonction.membre_actuel  # Utilise la @property du modèle
        if membre:
            bureau_membres.append({
                'fonction': fonction,
                'profil': membre,
            })

    context = {
        'bureau_membres': bureau_membres,
    }

    return render(request, 'members/bureau.html', context)


# ============================================
# DASHBOARD MEMBRE (Espace personnel)
# ============================================

@login_required
def dashboard(request):
    """
    Dashboard personnel du membre connecté
    Affiche : profil, inscriptions événements, statistiques
    """
    # Récupérer ou créer le profil du membre
    try:
        profil = request.user.profil
    except ProfilMembre.DoesNotExist:
        messages.warning(request, "Votre profil n'a pas encore été créé. Contactez l'administration.")
        return redirect('core:home')

    # Récupérer les inscriptions aux événements
    from django.utils import timezone

    # Inscriptions futures
    inscriptions_futures = Inscription.objects.filter(
        participant=request.user,
        evenement__date_debut__gte=timezone.now()
    ).select_related('evenement', 'evenement__lieu', 'evenement__type_evenement').order_by('evenement__date_debut')

    # Inscriptions passées
    inscriptions_passees = Inscription.objects.filter(
        participant=request.user,
        evenement__date_debut__lt=timezone.now()
    ).select_related('evenement').order_by('-evenement__date_debut')[:5]

    # Statistiques
    total_inscriptions = Inscription.objects.filter(participant=request.user).count()
    total_presences = Inscription.objects.filter(participant=request.user, present=True).count()
    taux_presence = (total_presences / total_inscriptions * 100) if total_inscriptions > 0 else 0

    context = {
        'profil': profil,
        'inscriptions_futures': inscriptions_futures,
        'inscriptions_passees': inscriptions_passees,
        'total_inscriptions': total_inscriptions,
        'total_presences': total_presences,
        'taux_presence': round(taux_presence, 1),
    }

    return render(request, 'members/dashboard.html', context)


# ============================================
# MODIFICATION PROFIL
# ============================================

@login_required
def profil_modifier(request):
    """
    Permet au membre de modifier son profil
    """
    try:
        profil = request.user.profil
    except ProfilMembre.DoesNotExist:
        messages.warning(request, "Votre profil n'a pas encore été créé. Contactez l'administration.")
        return redirect('core:home')

    if request.method == 'POST':
        # Mise à jour du User
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        # Mise à jour du ProfilMembre
        profil.telephone = request.POST.get('telephone', '')
        profil.telephone_portable = request.POST.get('telephone_portable', '')
        profil.adresse = request.POST.get('adresse', '')
        profil.code_postal = request.POST.get('code_postal', '')
        profil.ville = request.POST.get('ville', '')
        profil.bio = request.POST.get('bio', '')
        profil.experience_aeromodelisme = request.POST.get('experience_aeromodelisme', '')
        profil.specialites = request.POST.get('specialites', '')
        profil.avions_possedes = request.POST.get('avions_possedes', '')

        # Réseaux sociaux
        profil.site_web = request.POST.get('site_web', '')
        profil.youtube = request.POST.get('youtube', '')
        profil.facebook = request.POST.get('facebook', '')
        profil.instagram = request.POST.get('instagram', '')

        # Préférences
        profil.newsletter = request.POST.get('newsletter') == 'on'
        profil.notifications_evenements = request.POST.get('notifications_evenements') == 'on'
        profil.profil_public = request.POST.get('profil_public') == 'on'

        # Gestion de la photo
        if 'photo' in request.FILES:
            profil.photo = request.FILES['photo']

        profil.save()

        messages.success(request, "Votre profil a été mis à jour avec succès !")
        return redirect('members:dashboard')

    context = {
        'profil': profil,
    }

    return render(request, 'members/profil_modifier.html', context)
