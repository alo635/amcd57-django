"""
Sitemaps pour le référencement SEO du site AMCD57
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Article
from events.models import Evenement
from weblinks.models import Lien


class StaticViewSitemap(Sitemap):
    """Sitemap pour les pages statiques"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:contact',
            'core:mentions_legales',
            'core:politique_confidentialite',
            'core:cgu',
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    """Sitemap pour les articles de blog"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.filter(statut='publie').order_by('-date_publication')

    def lastmod(self, obj):
        return obj.date_modification


class EventSitemap(Sitemap):
    """Sitemap pour les événements"""
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Evenement.objects.filter(statut__in=['planifie', 'confirme']).order_by('-date_debut')

    def lastmod(self, obj):
        return obj.date_modification


class WeblinksSitemap(Sitemap):
    """Sitemap pour les liens utiles"""
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Lien.objects.filter(actif=True).order_by('-date_ajout')

    def lastmod(self, obj):
        return obj.date_modification
