"""
Configuration Gunicorn pour AMCD57
Documentation : https://docs.gunicorn.org/en/stable/settings.html
"""

import multiprocessing
import os

# ========================================
# Bind - Adresse et port
# ========================================
# Écoute sur localhost uniquement (Nginx fera le proxy)
bind = "127.0.0.1:8000"

# ========================================
# Workers
# ========================================
# Nombre de workers (recommandation : (2 x CPU) + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Type de worker
worker_class = "sync"

# Nombre max de connexions simultanées par worker
worker_connections = 1000

# Timeout : temps max pour traiter une requête (secondes)
timeout = 30

# Keepalive : temps de maintien des connexions (secondes)
keepalive = 2

# ========================================
# Logging
# ========================================
# Chemin vers les logs (à adapter si nécessaire)
accesslog = "/var/www/amcd57/logs/gunicorn-access.log"
errorlog = "/var/www/amcd57/logs/gunicorn-error.log"

# Niveau de log : debug, info, warning, error, critical
loglevel = "info"

# Format des logs d'accès
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# ========================================
# Process naming
# ========================================
proc_name = "amcd57_gunicorn"

# ========================================
# Server mechanics
# ========================================
# Ne pas lancer en daemon (systemd gère ça)
daemon = False

# Fichier PID
pidfile = "/var/www/amcd57/gunicorn.pid"

# Utilisateur et groupe (pour la sécurité)
user = "amcd"
group = "amcd"

# ========================================
# Security
# ========================================
# Limite de la taille de la ligne de requête
limit_request_line = 4096

# Nombre max de champs d'en-tête
limit_request_fields = 100

# Taille max d'un champ d'en-tête
limit_request_field_size = 8190

# ========================================
# Server hooks (optionnel)
# ========================================
def on_starting(server):
    """
    Appelé juste avant que le serveur ne démarre
    """
    server.log.info("🚀 Démarrage de Gunicorn pour AMCD57...")

def on_reload(server):
    """
    Appelé lors d'un reload
    """
    server.log.info("🔄 Rechargement de Gunicorn...")

def when_ready(server):
    """
    Appelé quand le serveur est prêt à accepter des connexions
    """
    server.log.info("✅ Gunicorn est prêt - AMCD57 en ligne !")

def worker_int(worker):
    """
    Appelé quand un worker reçoit un SIGINT ou SIGQUIT
    """
    worker.log.info("🛑 Worker interrompu (PID: %s)", worker.pid)

def worker_abort(worker):
    """
    Appelé quand un worker est tué
    """
    worker.log.info("💀 Worker abandonné (PID: %s)", worker.pid)
