"""
Vues pour l'application Blog AMCD57
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Article, Categorie, Tag, Commentaire


# ============================================
# LISTE DES ARTICLES
# ============================================

def article_list(request):
    """
    Affiche la liste des articles publiés
    URL : /blog/
    """
    # Récupère tous les articles publiés, triés par date décroissante
    articles = Article.objects.filter(statut='publie').order_by('-date_publication')
    
    # Recherche (optionnel)
    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(titre__icontains=query) |
            Q(contenu__icontains=query) |
            Q(extrait__icontains=query)
        )
    
    # Pagination : 9 articles par page
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Catégories pour le menu
    categories = Categorie.objects.all()
    
    # Articles récents pour la sidebar
    articles_recents = Article.objects.filter(statut='publie').order_by('-date_publication')[:5]
    
    # Tags populaires (top 10)
    tags = Tag.objects.all()[:10]
    
    context = {
        'page_obj': page_obj,
        'articles': page_obj,  # Alias pour simplicité dans le template
        'categories': categories,
        'articles_recents': articles_recents,
        'tags': tags,
        'query': query,
    }
    
    return render(request, 'blog/article_list.html', context)


# ============================================
# DÉTAIL D'UN ARTICLE
# ============================================

def article_detail(request, slug):
    """
    Affiche le détail d'un article
    URL : /blog/<slug>/
    """
    # Récupère l'article par son slug
    article = get_object_or_404(Article, slug=slug, statut='publie')
    
    # Incrémente le compteur de vues
    article.incrementer_vues()
    
    # Récupère les commentaires approuvés
    commentaires = article.commentaires.filter(
        approuve=True,
        parent=None  # Uniquement les commentaires principaux (pas les réponses)
    ).order_by('date_creation')
    
    # Articles similaires (même catégorie)
    articles_similaires = Article.objects.filter(
        categorie=article.categorie,
        statut='publie'
    ).exclude(pk=article.pk).order_by('-date_publication')[:3]
    
    # Gestion du formulaire de commentaire (si POST)
    if request.method == 'POST':
        # Récupère les données du formulaire
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        contenu = request.POST.get('contenu')
        parent_id = request.POST.get('parent_id')
        
        # Validation simple
        if nom and email and contenu:
            # Crée le commentaire
            commentaire = Commentaire(
                article=article,
                auteur_nom=nom,
                auteur_email=email,
                contenu=contenu,
                approuve=False  # En attente de modération
            )
            
            # Si l'utilisateur est connecté, lie le commentaire
            if request.user.is_authenticated:
                commentaire.auteur_user = request.user
                commentaire.auteur_nom = request.user.get_full_name() or request.user.username
                commentaire.auteur_email = request.user.email
            
            # Si c'est une réponse à un commentaire
            if parent_id:
                parent = get_object_or_404(Commentaire, pk=parent_id)
                commentaire.parent = parent
            
            commentaire.save()
            
            messages.success(request, 'Votre commentaire a été envoyé et sera publié après modération.')
            return redirect('blog:article_detail', slug=slug)
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    context = {
        'article': article,
        'commentaires': commentaires,
        'articles_similaires': articles_similaires,
    }
    
    return render(request, 'blog/article_detail.html', context)


# ============================================
# ARTICLES PAR CATÉGORIE
# ============================================

def categorie_detail(request, slug):
    """
    Affiche les articles d'une catégorie
    URL : /blog/categorie/<slug>/
    """
    # Récupère la catégorie
    categorie = get_object_or_404(Categorie, slug=slug)
    
    # Récupère les articles de cette catégorie
    articles = Article.objects.filter(
        categorie=categorie,
        statut='publie'
    ).order_by('-date_publication')
    
    # Pagination
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Toutes les catégories pour le menu
    categories = Categorie.objects.all()
    
    context = {
        'categorie': categorie,
        'page_obj': page_obj,
        'articles': page_obj,
        'categories': categories,
    }
    
    return render(request, 'blog/categorie_detail.html', context)


# ============================================
# ARTICLES PAR TAG
# ============================================

def tag_detail(request, slug):
    """
    Affiche les articles d'un tag
    URL : /blog/tag/<slug>/
    """
    # Récupère le tag
    tag = get_object_or_404(Tag, slug=slug)
    
    # Récupère les articles avec ce tag
    articles = Article.objects.filter(
        tags=tag,
        statut='publie'
    ).order_by('-date_publication')
    
    # Pagination
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Catégories pour le menu
    categories = Categorie.objects.all()
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'articles': page_obj,
        'categories': categories,
    }
    
    return render(request, 'blog/tag_detail.html', context)


# ============================================
# RECHERCHE
# ============================================

def article_search(request):
    """
    Recherche dans les articles
    URL : /blog/recherche/
    """
    query = request.GET.get('q', '')
    
    if query:
        articles = Article.objects.filter(
            Q(titre__icontains=query) |
            Q(contenu__icontains=query) |
            Q(extrait__icontains=query),
            statut='publie'
        ).order_by('-date_publication')
    else:
        articles = Article.objects.none()
    
    # Pagination
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'articles': page_obj,
        'nombre_resultats': articles.count(),
    }
    
    return render(request, 'blog/article_search.html', context)