# Plan : Dashboard de Monitoring et Analytics

## 🎯 Objectif

Créer un **centre de contrôle** dans l'admin Django pour monitorer la santé et l'activité du site AMCD57 avec :
- Statistiques d'accès et de consultation
- Métriques Fail2ban (IPs bannies, tentatives d'intrusion)
- Santé du système (CPU, RAM, disque)
- Activité utilisateurs et contenu
- Logs en temps réel

---

## 📊 Fonctionnalités proposées

### 1. Statistiques du site

#### A. Visiteurs et trafic
- **Visiteurs uniques** (jour, semaine, mois)
- **Pages vues** totales
- **Pages les plus consultées**
- **Graphique d'évolution** du trafic
- **Temps moyen** sur le site
- **Taux de rebond**

#### B. Contenu populaire
- **Articles les plus lus** (top 10 avec nombre de vues)
- **Événements les plus consultés**
- **Catégories les plus visitées**
- **Tags populaires**

#### C. Activité utilisateurs
- **Membres connectés** aujourd'hui
- **Nouvelles inscriptions** (semaine/mois)
- **Inscriptions aux événements** récentes
- **Commentaires** en attente de modération

### 2. Sécurité (Fail2ban)

- **IPs actuellement bannies** (nombre + liste)
- **Tentatives d'intrusion** bloquées (24h, 7j, 30j)
- **Jails actifs** et leur statut
- **Dernières attaques** détectées (IP, date, jail)
- **Graphique des bannissements** par jour
- **Top 10 des IPs malveillantes**

### 3. Santé du système

- **Espace disque** (total, utilisé, libre)
- **Utilisation RAM** (%)
- **Charge CPU** (%)
- **Uptime** du serveur
- **Services actifs** (Gunicorn, Nginx, Fail2ban)
- **Dernière mise à jour** du site

### 4. Performance

- **Temps de réponse moyen** des pages
- **Requêtes lentes** (si activées)
- **Cache hit rate** (si applicable)
- **Taille de la base de données**

### 5. Logs en temps réel

- **Dernières erreurs** (Django error log)
- **Accès récents** (Nginx access log - 50 derniers)
- **Activités admin** (qui a fait quoi)

---

## 🛠️ Architecture technique

### Technologies recommandées

#### Option 1 : Solution simple et rapide ⭐ (RECOMMANDÉ)
**Stack :**
- **Django Admin** natif avec vues personnalisées
- **Chart.js** pour les graphiques (via CDN)
- **psutil** pour les métriques système (Python)
- **Parsing des logs** Fail2ban et Nginx
- **Modèles Django** pour stocker les statistiques

**Avantages :**
✅ Pas de dépendances lourdes
✅ Intégration parfaite avec l'admin existant
✅ Contrôle total du code
✅ Léger et performant

#### Option 2 : Solution avancée avec package
**Packages Django disponibles :**
- **django-db-logger** - Logs en base de données
- **django-analytics** - Tracking des visiteurs
- **django-prometheus** - Métriques système avancées

**Avantages :**
✅ Fonctionnalités prêtes à l'emploi
❌ Dépendances supplémentaires
❌ Moins de flexibilité

### Ma recommandation : **Option 1**

Développer un dashboard custom intégré à l'admin Django avec Chart.js pour les graphiques.

---

## 🎯 APPROCHE : MVP D'ABORD (Recommandé)

Pour cette fonctionnalité complexe, nous allons procéder en **3 phases progressives** :

1. **Phase MVP** (5-7h) - Version minimale viable, fonctionnelle rapidement
2. **Phase 2** (4-5h) - Graphiques et améliorations visuelles
3. **Phase 3** (5-6h) - Fonctionnalités avancées (optionnel)

**Total : 14-18h de développement**

---

## 🚀 PHASE MVP : Version Minimale Viable (PRIORITÉ)

**Durée : 5-7h | Objectif : Dashboard opérationnel rapidement**

### Fonctionnalités MVP

#### 1. Tracking basique des visites 📈
- Middleware pour enregistrer automatiquement les pages vues
- Modèle `PageView` simple : URL, user, IP, timestamp, response_time
- Statistiques : total pages vues, visiteurs uniques (7j et 30j)

#### 2. Santé du système 💻
- Utilisation disque (total, utilisé, libre, %)
- Utilisation RAM (%)
- Utilisation CPU (%)
- Uptime du serveur
- Statut des services (Gunicorn, Nginx, Fail2ban) - ON/OFF uniquement

#### 3. Statistiques de contenu 📝
- Nombre total d'articles publiés
- Nombre total d'événements
- Nombre de membres actifs
- Top 5 articles les plus lus

#### 4. Sécurité Fail2ban basique 🔒
- Nombre d'IPs actuellement bannies (depuis la BDD)
- Liste des 10 dernières IPs bannies avec jail et date

#### 5. Interface dashboard simple
- Page accessible depuis `/analytics/dashboard/`
- Lien visible sur la page d'accueil de l'admin
- Design simple avec cartes de statistiques
- **Pas de graphiques Chart.js dans le MVP** (juste chiffres et barres CSS)
- Responsive pour mobile

### Architecture MVP simplifiée

```
analytics/
├── models.py
│   └── PageView (uniquement)
├── middleware.py
│   └── AnalyticsMiddleware
├── services.py
│   ├── AnalyticsService (stats visiteurs et contenu)
│   ├── SystemHealthService (métriques système)
│   └── Fail2banService (basique, lit les PageView pour IPs)
├── views.py
│   └── dashboard_view
├── templates/analytics/
│   └── dashboard.html (simple, pas de Chart.js)
└── admin.py
    └── PageViewAdmin
```

### Étapes MVP

1. **Créer l'app analytics** (15min)
2. **Créer modèle PageView + migrations** (30min)
3. **Implémenter middleware de tracking** (1h)
4. **Créer services (Analytics, SystemHealth, Fail2ban basique)** (2h)
5. **Créer vue dashboard_view** (30min)
6. **Créer template simple sans graphiques** (1-2h)
7. **Ajouter lien dans admin Django** (30min)
8. **Tests et ajustements** (1h)

**Total MVP : 5-7h**

---

## 📊 PHASE 2 : Graphiques et améliorations visuelles

**Durée : 4-5h | Après validation du MVP**

### Ajouts Phase 2

#### 1. Graphiques Chart.js 📈
- Intégration Chart.js (via CDN)
- Graphique évolution du trafic (30 jours)
  - Courbe pages vues
  - Courbe visiteurs uniques
- Graphique bannissements Fail2ban
- Graphique répartition des visites par page

#### 2. Modèle DailyStats
- Agrégation quotidienne des statistiques
- Champs : date, unique_visitors, page_views, new_members, new_articles, etc.
- Commande Django `aggregate_daily_stats`
- Cron job pour automatisation

#### 3. Pages populaires détaillées
- Tableau des 20 pages les plus visitées
- Temps de réponse moyen par page

#### 4. Design amélioré
- Dégradés cohérents avec le site
- Animations CSS
- Icônes pour sections
- Organisation visuelle optimisée

---

## 🎨 PHASE 3 : Fonctionnalités avancées (Optionnel)

**Durée : 5-6h | Quand MVP et Phase 2 sont stables**

### Ajouts Phase 3

#### 1. Analytics avancées
- Répartition par navigateur
- Répartition par device (mobile/tablet/desktop)
- Pages de référence
- Temps moyen par session
- Taux de rebond

#### 2. Fail2ban avancé
- Modèle `Fail2banLog` complet
- Parser automatique du log Fail2ban
- Graphiques par jail
- Carte géographique des IPs (géolocalisation API)

#### 3. Monitoring temps réel
- Rafraîchissement auto (AJAX)
- Logs en temps réel (50 dernières lignes Nginx)
- Alertes visuelles (warning si disque > 80%)

#### 4. Export et rapports
- Export PDF statistiques mensuelles
- Export CSV données brutes
- Email automatique rapport hebdomadaire

---

## 📋 Plan d'implémentation MVP (Détaillé)

### Étape 1 : Créer l'app analytics (15min)

#### 1.1 Créer une nouvelle app `analytics`

```bash
python manage.py startapp analytics
```

#### 1.2 Créer les modèles de tracking

**`analytics/models.py`** :

```python
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PageView(models.Model):
    """Tracking des pages vues"""
    url = models.CharField(max_length=500)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500, blank=True)
    referer = models.CharField(max_length=500, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    response_time = models.IntegerField(null=True, help_text="Temps de réponse en ms")

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'url']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.url} - {self.timestamp}"

class DailyStats(models.Model):
    """Statistiques agrégées par jour"""
    date = models.DateField(unique=True, db_index=True)
    unique_visitors = models.IntegerField(default=0)
    page_views = models.IntegerField(default=0)
    new_members = models.IntegerField(default=0)
    new_articles = models.IntegerField(default=0)
    new_events = models.IntegerField(default=0)
    comments_posted = models.IntegerField(default=0)
    event_registrations = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']
        verbose_name = "Statistique journalière"
        verbose_name_plural = "Statistiques journalières"

    def __str__(self):
        return f"Stats du {self.date}"

class Fail2banLog(models.Model):
    """Logs des bannissements Fail2ban"""
    ip_address = models.GenericIPAddressField(db_index=True)
    jail = models.CharField(max_length=50, db_index=True)
    action = models.CharField(max_length=20, choices=[
        ('ban', 'Bannissement'),
        ('unban', 'Débannissement'),
    ])
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Log Fail2ban"
        verbose_name_plural = "Logs Fail2ban"

    def __str__(self):
        return f"{self.ip_address} - {self.jail} - {self.action}"
```

#### 1.3 Migrations

```bash
python manage.py makemigrations analytics
python manage.py migrate analytics
```

---

### Phase 2 : Middleware de tracking (1-2h)

**`analytics/middleware.py`** :

```python
import time
from django.utils.deprecation import MiddlewareMixin
from .models import PageView

class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware pour tracker les visites"""

    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        # Ne pas tracker les requêtes admin, static, media
        if request.path.startswith(('/admin/', '/static/', '/media/')):
            return response

        # Ne pas tracker les méthodes non-GET
        if request.method != 'GET':
            return response

        # Calculer le temps de réponse
        response_time = None
        if hasattr(request, '_start_time'):
            response_time = int((time.time() - request._start_time) * 1000)

        # Enregistrer la page vue (de manière asynchrone si possible)
        try:
            PageView.objects.create(
                url=request.path,
                user=request.user if request.user.is_authenticated else None,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                referer=request.META.get('HTTP_REFERER', '')[:500],
                session_key=request.session.session_key or '',
                response_time=response_time,
            )
        except Exception as e:
            # Ne pas bloquer la requête si le tracking échoue
            pass

        return response

    @staticmethod
    def get_client_ip(request):
        """Récupère l'IP réelle du client (même derrière proxy)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

**Ajouter le middleware dans `settings.py`** :

```python
MIDDLEWARE = [
    # ... middlewares existants
    'analytics.middleware.AnalyticsMiddleware',  # Ajouter en dernier
]
```

---

### Phase 3 : Services de collecte de données (2-3h)

**`analytics/services.py`** :

```python
import os
import re
import psutil
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from .models import PageView, DailyStats, Fail2banLog
from blog.models import Article
from events.models import Evenement, Inscription
from members.models import ProfilMembre

User = get_user_model()

class AnalyticsService:
    """Service pour récupérer les statistiques du site"""

    @staticmethod
    def get_visitor_stats(days=30):
        """Statistiques de visiteurs sur N jours"""
        since = timezone.now() - timedelta(days=days)

        total_views = PageView.objects.filter(timestamp__gte=since).count()
        unique_visitors = PageView.objects.filter(
            timestamp__gte=since
        ).values('ip_address').distinct().count()

        return {
            'total_views': total_views,
            'unique_visitors': unique_visitors,
            'avg_views_per_visitor': round(total_views / unique_visitors, 1) if unique_visitors > 0 else 0,
        }

    @staticmethod
    def get_popular_pages(limit=10):
        """Pages les plus consultées"""
        return PageView.objects.values('url').annotate(
            views=Count('id')
        ).order_by('-views')[:limit]

    @staticmethod
    def get_daily_stats(days=30):
        """Statistiques journalières pour graphiques"""
        since = timezone.now() - timedelta(days=days)
        return DailyStats.objects.filter(date__gte=since).order_by('date')

    @staticmethod
    def get_content_stats():
        """Statistiques sur le contenu"""
        return {
            'total_articles': Article.objects.filter(statut='publie').count(),
            'total_events': Evenement.objects.count(),
            'total_members': User.objects.filter(is_active=True).count(),
            'pending_comments': 0,  # À implémenter selon votre modèle
            'popular_articles': Article.objects.filter(
                statut='publie'
            ).order_by('-vues')[:5],
        }

class SystemHealthService:
    """Service pour la santé du système"""

    @staticmethod
    def get_disk_usage():
        """Utilisation du disque"""
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent,
        }

    @staticmethod
    def get_memory_usage():
        """Utilisation de la RAM"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
        }

    @staticmethod
    def get_cpu_usage():
        """Utilisation CPU"""
        return {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
        }

    @staticmethod
    def get_uptime():
        """Uptime du serveur"""
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        return {
            'seconds': int(uptime_seconds),
            'formatted': str(timedelta(seconds=int(uptime_seconds))),
        }

    @staticmethod
    def check_services():
        """Vérifier si les services sont actifs"""
        services = {}

        # Vérifier Gunicorn
        for proc in psutil.process_iter(['name']):
            if 'gunicorn' in proc.info['name'].lower():
                services['gunicorn'] = True
                break
        else:
            services['gunicorn'] = False

        # Vérifier Nginx
        for proc in psutil.process_iter(['name']):
            if 'nginx' in proc.info['name'].lower():
                services['nginx'] = True
                break
        else:
            services['nginx'] = False

        # Vérifier Fail2ban
        for proc in psutil.process_iter(['name']):
            if 'fail2ban' in proc.info['name'].lower():
                services['fail2ban'] = True
                break
        else:
            services['fail2ban'] = False

        return services

class Fail2banService:
    """Service pour les métriques Fail2ban"""

    @staticmethod
    def get_banned_ips():
        """Liste des IPs actuellement bannies"""
        # Cette méthode nécessite l'accès à fail2ban-client
        # En production, exécuter : fail2ban-client status [jail]
        # Pour l'instant, on lit depuis la base de données

        banned = Fail2banLog.objects.filter(
            action='ban'
        ).values('ip_address').annotate(
            ban_count=Count('id')
        ).order_by('-ban_count')

        return banned

    @staticmethod
    def get_ban_stats(days=30):
        """Statistiques de bannissements"""
        since = timezone.now() - timedelta(days=days)

        total_bans = Fail2banLog.objects.filter(
            action='ban',
            timestamp__gte=since
        ).count()

        bans_by_jail = Fail2banLog.objects.filter(
            action='ban',
            timestamp__gte=since
        ).values('jail').annotate(count=Count('id')).order_by('-count')

        return {
            'total_bans': total_bans,
            'bans_by_jail': bans_by_jail,
        }

    @staticmethod
    def parse_fail2ban_log():
        """Parser le log Fail2ban pour extraire les bannissements"""
        # Chemin du log Fail2ban
        log_path = '/var/log/fail2ban.log'

        if not os.path.exists(log_path):
            return []

        # Regex pour extraire les bannissements
        ban_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Ban (\d+\.\d+\.\d+\.\d+)')

        recent_bans = []
        try:
            with open(log_path, 'r') as f:
                # Lire les 1000 dernières lignes
                lines = f.readlines()[-1000:]
                for line in lines:
                    match = ban_pattern.search(line)
                    if match:
                        recent_bans.append({
                            'timestamp': match.group(1),
                            'ip': match.group(2),
                        })
        except PermissionError:
            # Pas d'accès au fichier en dev
            pass

        return recent_bans
```

---

### Phase 4 : Vue du dashboard (3-4h)

**`analytics/views.py`** :

```python
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .services import AnalyticsService, SystemHealthService, Fail2banService

@staff_member_required
def dashboard_view(request):
    """Vue principale du dashboard de monitoring"""

    # Statistiques visiteurs
    visitor_stats_30d = AnalyticsService.get_visitor_stats(days=30)
    visitor_stats_7d = AnalyticsService.get_visitor_stats(days=7)
    popular_pages = AnalyticsService.get_popular_pages(limit=10)
    daily_stats = AnalyticsService.get_daily_stats(days=30)
    content_stats = AnalyticsService.get_content_stats()

    # Santé système
    disk_usage = SystemHealthService.get_disk_usage()
    memory_usage = SystemHealthService.get_memory_usage()
    cpu_usage = SystemHealthService.get_cpu_usage()
    uptime = SystemHealthService.get_uptime()
    services_status = SystemHealthService.check_services()

    # Sécurité Fail2ban
    banned_ips = Fail2banService.get_banned_ips()
    ban_stats = Fail2banService.get_ban_stats(days=30)

    context = {
        'visitor_stats_30d': visitor_stats_30d,
        'visitor_stats_7d': visitor_stats_7d,
        'popular_pages': popular_pages,
        'daily_stats': daily_stats,
        'content_stats': content_stats,
        'disk_usage': disk_usage,
        'memory_usage': memory_usage,
        'cpu_usage': cpu_usage,
        'uptime': uptime,
        'services_status': services_status,
        'banned_ips': banned_ips,
        'ban_stats': ban_stats,
    }

    return render(request, 'analytics/dashboard.html', context)
```

**`analytics/urls.py`** :

```python
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
```

**Ajouter dans `amcd57_project/urls.py`** :

```python
urlpatterns = [
    # ... URLs existantes
    path('analytics/', include('analytics.urls')),
]
```

---

### Phase 5 : Template du dashboard (4-5h)

**`analytics/templates/analytics/dashboard.html`** :

```django
{% extends "admin/base_site.html" %}
{% load static %}

{% block title %}Dashboard de Monitoring - AMCD57{% endblock %}

{% block extrastyle %}
<style>
    .dashboard-container {
        padding: 20px;
    }
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    .stat-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-card h3 {
        margin: 0 0 15px 0;
        color: #417690;
        font-size: 1.1em;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
    }
    .stat-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #2c3e50;
        margin: 10px 0;
    }
    .stat-label {
        color: #666;
        font-size: 0.9em;
    }
    .progress-bar {
        height: 20px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s;
    }
    .service-status {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 10px 0;
    }
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    .status-active {
        background: #28a745;
    }
    .status-inactive {
        background: #dc3545;
    }
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    table.analytics-table {
        width: 100%;
        border-collapse: collapse;
    }
    table.analytics-table th,
    table.analytics-table td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
    }
    table.analytics-table th {
        background: #f5f5f5;
        font-weight: bold;
    }
</style>
{% endblock %}

{% block content %}
<div class="dashboard-container">
    <h1 style="margin-bottom: 30px;">📊 Dashboard de Monitoring</h1>

    <!-- Statistiques visiteurs -->
    <h2>👥 Statistiques visiteurs (30 derniers jours)</h2>
    <div class="dashboard-grid">
        <div class="stat-card">
            <h3>Pages vues</h3>
            <div class="stat-value">{{ visitor_stats_30d.total_views }}</div>
            <div class="stat-label">Au total</div>
        </div>
        <div class="stat-card">
            <h3>Visiteurs uniques</h3>
            <div class="stat-value">{{ visitor_stats_30d.unique_visitors }}</div>
            <div class="stat-label">IP distinctes</div>
        </div>
        <div class="stat-card">
            <h3>Pages/visiteur</h3>
            <div class="stat-value">{{ visitor_stats_30d.avg_views_per_visitor }}</div>
            <div class="stat-label">Moyenne</div>
        </div>
    </div>

    <!-- Graphique d'évolution (Chart.js) -->
    <div class="chart-container">
        <h3>Évolution du trafic (30 jours)</h3>
        <canvas id="trafficChart" height="80"></canvas>
    </div>

    <!-- Contenu populaire -->
    <h2>🔥 Contenu populaire</h2>
    <div class="stat-card">
        <h3>Articles les plus lus</h3>
        <table class="analytics-table">
            <thead>
                <tr>
                    <th>Article</th>
                    <th>Vues</th>
                </tr>
            </thead>
            <tbody>
                {% for article in content_stats.popular_articles %}
                <tr>
                    <td>{{ article.titre }}</td>
                    <td><strong>{{ article.vues }}</strong></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Santé système -->
    <h2>💻 Santé du système</h2>
    <div class="dashboard-grid">
        <div class="stat-card">
            <h3>Espace disque</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ disk_usage.percent }}%"></div>
            </div>
            <div class="stat-label">{{ disk_usage.percent }}% utilisé ({{ disk_usage.used|filesizeformat }} / {{ disk_usage.total|filesizeformat }})</div>
        </div>
        <div class="stat-card">
            <h3>Mémoire RAM</h3>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {{ memory_usage.percent }}%"></div>
            </div>
            <div class="stat-label">{{ memory_usage.percent }}% utilisé ({{ memory_usage.used|filesizeformat }} / {{ memory_usage.total|filesizeformat }})</div>
        </div>
        <div class="stat-card">
            <h3>CPU</h3>
            <div class="stat-value">{{ cpu_usage.percent }}%</div>
            <div class="stat-label">{{ cpu_usage.count }} cœurs</div>
        </div>
        <div class="stat-card">
            <h3>Uptime</h3>
            <div class="stat-value" style="font-size: 1.5em;">{{ uptime.formatted }}</div>
            <div class="stat-label">Temps de fonctionnement</div>
        </div>
    </div>

    <!-- Statut des services -->
    <div class="stat-card">
        <h3>Services actifs</h3>
        <div class="service-status">
            <div class="status-indicator {% if services_status.gunicorn %}status-active{% else %}status-inactive{% endif %}"></div>
            <span>Gunicorn (Django)</span>
        </div>
        <div class="service-status">
            <div class="status-indicator {% if services_status.nginx %}status-active{% else %}status-inactive{% endif %}"></div>
            <span>Nginx (Serveur web)</span>
        </div>
        <div class="service-status">
            <div class="status-indicator {% if services_status.fail2ban %}status-active{% else %}status-inactive{% endif %}"></div>
            <span>Fail2ban (Sécurité)</span>
        </div>
    </div>

    <!-- Sécurité Fail2ban -->
    <h2>🔒 Sécurité (Fail2ban)</h2>
    <div class="dashboard-grid">
        <div class="stat-card">
            <h3>Bannissements (30j)</h3>
            <div class="stat-value">{{ ban_stats.total_bans }}</div>
            <div class="stat-label">IPs bloquées</div>
        </div>
        <div class="stat-card">
            <h3>IPs actuellement bannies</h3>
            <div class="stat-value">{{ banned_ips|length }}</div>
            <div class="stat-label">Actives</div>
        </div>
    </div>

    <div class="stat-card">
        <h3>Top IPs malveillantes</h3>
        <table class="analytics-table">
            <thead>
                <tr>
                    <th>IP</th>
                    <th>Nombre de bannissements</th>
                </tr>
            </thead>
            <tbody>
                {% for ban in banned_ips|slice:":10" %}
                <tr>
                    <td><code>{{ ban.ip_address }}</code></td>
                    <td><strong>{{ ban.ban_count }}</strong></td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="2" style="text-align: center; color: #999;">Aucun bannissement enregistré</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
// Graphique d'évolution du trafic
const ctx = document.getElementById('trafficChart');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: [
            {% for stat in daily_stats %}
                '{{ stat.date|date:"d/m" }}'{% if not forloop.last %},{% endif %}
            {% endfor %}
        ],
        datasets: [{
            label: 'Pages vues',
            data: [
                {% for stat in daily_stats %}
                    {{ stat.page_views }}{% if not forloop.last %},{% endif %}
                {% endfor %}
            ],
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4
        }, {
            label: 'Visiteurs uniques',
            data: [
                {% for stat in daily_stats %}
                    {{ stat.unique_visitors }}{% if not forloop.last %},{% endif %}
                {% endfor %}
            ],
            borderColor: '#764ba2',
            backgroundColor: 'rgba(118, 75, 162, 0.1)',
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
</script>
{% endblock %}
```

---

### Phase 6 : Lien dans l'admin Django (30min)

**`analytics/admin.py`** :

```python
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import PageView, DailyStats, Fail2banLog

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'user', 'ip_address', 'timestamp', 'response_time']
    list_filter = ['timestamp', 'user']
    search_fields = ['url', 'ip_address']
    readonly_fields = ['url', 'user', 'ip_address', 'user_agent', 'referer', 'timestamp', 'response_time']

    def has_add_permission(self, request):
        return False  # Pas d'ajout manuel

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'unique_visitors', 'page_views', 'new_members', 'new_articles']
    list_filter = ['date']
    readonly_fields = ['date']

@admin.register(Fail2banLog)
class Fail2banLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'jail', 'action', 'timestamp']
    list_filter = ['jail', 'action', 'timestamp']
    search_fields = ['ip_address']
    readonly_fields = ['ip_address', 'jail', 'action', 'timestamp']

    def has_add_permission(self, request):
        return False
```

**Ajouter un lien dans l'admin** :

Dans `amcd57_project/admin.py` (créer si n'existe pas) :

```python
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Personnaliser l'index de l'admin
admin.site.index_template = 'admin/custom_index.html'
```

**Template `templates/admin/custom_index.html`** :

```django
{% extends "admin/index.html" %}

{% block content %}
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
    <h2 style="color: white; margin: 0 0 10px 0;">📊 Centre de contrôle</h2>
    <a href="{% url 'analytics:dashboard' %}" style="background: white; color: #667eea; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; display: inline-block;">
        Accéder au Dashboard de Monitoring →
    </a>
</div>

{{ block.super }}
{% endblock %}
```

---

## 📦 Dépendances requises

**Ajouter dans `requirements.txt`** :

```txt
psutil==5.9.6  # Pour les métriques système
```

**Installer** :

```bash
pip install psutil==5.9.6
```

---

## 🚀 Déploiement

### En développement

1. Créer l'app `analytics`
2. Ajouter les modèles
3. Migrer la base de données
4. Activer le middleware
5. Créer les templates
6. Tester le dashboard

### En production

**Permissions pour accéder aux logs Fail2ban** :

```bash
# Ajouter l'utilisateur Django au groupe adm (pour lire les logs)
sudo usermod -a -G adm amcd

# Donner accès en lecture au log Fail2ban
sudo chmod 644 /var/log/fail2ban.log
```

**Commande cron pour agréger les stats** :

Créer une commande Django pour calculer les `DailyStats` :

```bash
# Ajouter au crontab
0 1 * * * cd /var/www/amcd57 && /var/www/amcd57/venv/bin/python manage.py aggregate_daily_stats
```

---

## 📊 Captures d'écran mockup

Le dashboard ressemblera à ceci :

```
┌─────────────────────────────────────────────────────┐
│ 📊 Dashboard de Monitoring                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 👥 Statistiques visiteurs (30 derniers jours)      │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│ │ 1,234    │  │ 456      │  │ 2.7      │          │
│ │ Pages    │  │ Visiteurs│  │ Pages/   │          │
│ │ vues     │  │ uniques  │  │ visiteur │          │
│ └──────────┘  └──────────┘  └──────────┘          │
│                                                     │
│ Évolution du trafic (30 jours)                     │
│ [Graphique Chart.js ligne]                         │
│                                                     │
│ 🔥 Articles les plus lus                           │
│ [Tableau avec top 5 articles]                      │
│                                                     │
│ 💻 Santé du système                                │
│ [Barres de progression disque/RAM/CPU]             │
│                                                     │
│ 🔒 Sécurité Fail2ban                               │
│ [Tableau IPs bannies + statistiques]               │
└─────────────────────────────────────────────────────┘
```

---

## ⏱️ Estimation du temps de développement

| Phase | Durée estimée |
|-------|---------------|
| Phase 1 : Modèles | 2-3h |
| Phase 2 : Middleware | 1-2h |
| Phase 3 : Services | 2-3h |
| Phase 4 : Vues | 1-2h |
| Phase 5 : Templates | 4-5h |
| Phase 6 : Admin | 30min |
| Tests et ajustements | 2-3h |
| **TOTAL** | **13-18h** |

---

## ✅ Checklist de réalisation

- [ ] Créer l'app `analytics`
- [ ] Créer les modèles (PageView, DailyStats, Fail2banLog)
- [ ] Créer les migrations
- [ ] Implémenter le middleware de tracking
- [ ] Créer les services (Analytics, SystemHealth, Fail2ban)
- [ ] Créer la vue dashboard
- [ ] Créer le template avec Chart.js
- [ ] Ajouter le lien dans l'admin
- [ ] Installer psutil
- [ ] Tester en développement
- [ ] Créer commande d'agrégation daily_stats
- [ ] Configurer cron pour agrégation
- [ ] Tester en production
- [ ] Documenter dans readme.md

---

## 🎯 Évolutions futures possibles

- **Export PDF** des rapports
- **Alertes email** (disque > 90%, trop d'attaques, etc.)
- **API REST** pour monitoring externe
- **Graphiques plus avancés** (répartition géographique, devices, navigateurs)
- **Intégration Google Analytics** (optionnel)
- **Logs en temps réel** avec WebSockets

---

**Voulez-vous que je commence l'implémentation de ce dashboard ?**

Options possibles :
1. Commencer directement l'implémentation complète
2. Créer une version simplifiée d'abord (MVP)
3. Créer une issue GitHub détaillée pour planifier
4. Autre approche ?

Qu'en pensez-vous ? 🚀
