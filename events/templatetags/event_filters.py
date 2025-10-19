"""
Template tags et filtres personnalisés pour l'app Events
"""

from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Divise une chaîne selon un délimiteur
    Usage: {{ "Lun,Mar,Mer"|split:"," }}
    """
    return value.split(delimiter)