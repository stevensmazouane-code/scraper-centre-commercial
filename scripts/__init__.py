"""
Package scripts - Scraper Centre Commercial
"""

__version__ = '1.0.0'
__author__ = 'EPSI - Atelier Collecte de Données'

from .scraper import CentrCommercialScraper
from .parser import StaticParser, DynamicParser

__all__ = [
    'CentrCommercialScraper',
    'StaticParser',
    'DynamicParser'
]
