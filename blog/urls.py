"""
URLs de l'application Blog
"""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Liste des articles : /blog/
    path('', views.article_list, name='article_list'),
    
    # Recherche : /blog/recherche/
    path('recherche/', views.article_search, name='article_search'),
    
    # Catégorie : /blog/categorie/club/
    path('categorie/<slug:slug>/', views.categorie_detail, name='categorie_detail'),
    
    # Tag : /blog/tag/planeur/
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    
    # Détail article : /blog/mon-article/
    path('<slug:slug>/', views.article_detail, name='article_detail'),
]