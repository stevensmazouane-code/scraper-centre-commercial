"""
Scraper générique pour centres commerciaux
Supporte sites statiques et dynamiques
"""
import requests
import logging
import json
import pandas as pd
from datetime import datetime
from parser import StaticParser, DynamicParser
from utils import setup_directories, save_raw_data, log_error, get_execution_stats

logger = logging.getLogger(__name__)


class CentrCommercialScraper:
    """
    Scraper générique pour extraire les magasins d'un centre commercial
    """
    
    def __init__(self, config_file=None):
        """
        Initialise le scraper
        
        Args:
            config_file: Chemin vers un fichier de configuration JSON
        """
        setup_directories()
        self.config = self._load_config(config_file) if config_file else {}
        self.session = self._setup_session()
        self.data_processed = []
        
    def _load_config(self, config_file):
        """Charge la configuration depuis un fichier JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"Configuration chargée depuis {config_file}")
            return config
        except FileNotFoundError:
            logger.warning(f"Fichier de configuration non trouvé: {config_file}")
            return {}
    
    def _setup_session(self):
        """Configure une session requests avec headers appropriés"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36')
        })
        return session
    
    def fetch_page(self, url):
        """
        Récupère le contenu HTML d'une page
        
        Args:
            url: URL à scraper
            
        Returns:
            str: Contenu HTML ou None en cas d'erreur
        """
        try:
            logger.info(f"Récupération de {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Page récupérée avec succès (Status: {response.status_code})")
            return response.text
            
        except requests.exceptions.Timeout:
            log_error('NetworkError', 'Timeout lors de la récupération', {'url': url})
            return None
        except requests.exceptions.ConnectionError:
            log_error('NetworkError', 'Erreur de connexion', {'url': url})
            return None
        except requests.exceptions.HTTPError as e:
            log_error('HTTPError', f"Erreur HTTP: {e.response.status_code}", {'url': url})
            return None
        except Exception as e:
            log_error('UnknownError', str(e), {'url': url})
            return None
    
    def parse_static(self, html_content, url, selectors):
        """
        Parse un site statique
        
        Args:
            html_content: Contenu HTML
            url: URL source
            selectors: Dict des sélecteurs CSS
            
        Returns:
            list: Liste des magasins parsés
        """
        parser = StaticParser(html_content, url)
        magasins = parser.parse_generic(selectors)
        
        # Sauvegarder les données brutes
        save_raw_data(magasins, 'magasins_raw.json', url)
        
        return magasins
    
    def parse_dynamic(self, url, wait_selector=None, selectors=None):
        """
        Parse un site dynamique avec Selenium
        
        Args:
            url: URL du site
            wait_selector: Sélecteur CSS à attendre
            selectors: Dict des sélecteurs CSS pour l'extraction
            
        Returns:
            list: Liste des magasins parsés
        """
        try:
            html_content = DynamicParser.parse_with_selenium(url, wait_selector)
            parser = DynamicParser(html_content, url)
            magasins = parser.parse_generic(selectors or {})
            
            # Sauvegarder les données brutes
            save_raw_data(magasins, 'magasins_raw_dynamic.json', url)
            
            return magasins
            
        except Exception as e:
            log_error('DynamicParsingError', str(e), {'url': url})
            return []
    
    def process_data(self, magasins):
        """
        Traite et nettoie les données
        
        Args:
            magasins: Liste des magasins bruts
            
        Returns:
            list: Données traitées
        """
        processed = []
        
        for magasin in magasins:
            # Normaliser les données
            item = {
                'nom': (magasin.get('nom') or '').strip(),
                'categorie': (magasin.get('categorie') or 'Non spécifiée').strip(),
                'horaires': magasin.get('horaires'),
                'localisation': magasin.get('localisation'),
                'date_extraction': datetime.now().strftime('%Y-%m-%d'),
                'source_url': magasin.get('source_url'),
                'extraction_id': magasin.get('extraction_id')
            }
            
            # Classifier la catégorie si possible
            item['categorie_normalisee'] = self._classify_category(item['categorie'])
            
            processed.append(item)
        
        self.data_processed = processed
        logger.info(f"{len(processed)} magasins traités")
        
        return processed
    
    def _classify_category(self, categorie):
        """
        Classe les catégories de magasins
        
        Args:
            categorie: Catégorie brute
            
        Returns:
            str: Catégorie normalisée
        """
        categorie_lower = categorie.lower()
        
        categories_map = {
            'Mode': ['vêtement', 'chaussure', 'fashion', 'zara', 'h&m', 'uniqlo', 'mode'],
            'Électronique': ['électronique', 'informatique', 'tech', 'apple', 'samsung'],
            'Hyper/Supermarché': ['carrefour', 'auchan', 'leclerc', 'intermarché', 'super', 'hyper'],
            'Loisirs': ['loisir', 'jouet', 'sport', 'décathlon', 'jeux'],
            'Beauté': ['beauté', 'cosmétique', 'parfum', 'pharmacie'],
            'Alimentation': ['restaurant', 'café', 'boulangerie', 'restauration']
        }
        
        for cat_norm, keywords in categories_map.items():
            if any(keyword in categorie_lower for keyword in keywords):
                return cat_norm
        
        return 'Autre'
    
    def export_csv(self, filename='output/magasins.csv'):
        """
        Exporte les données en CSV
        
        Args:
            filename: Chemin du fichier CSV
        """
        df = pd.DataFrame(self.data_processed)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Données exportées en CSV: {filename}")
        return filename
    
    def export_json(self, filename='output/magasins.json'):
        """
        Exporte les données en JSON
        
        Args:
            filename: Chemin du fichier JSON
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data_processed, f, ensure_ascii=False, indent=2)
        logger.info(f"Données exportées en JSON: {filename}")
        return filename
    
    def generate_report(self):
        """Génère un rapport d'exécution"""
        report = {
            'execution_stats': get_execution_stats(),
            'total_magasins': len(self.data_processed),
            'categories': {},
            'data_file': 'output/magasins.csv',
            'raw_data_file': 'data/raw/magasins_raw.json'
        }
        
        # Compter par catégorie
        for magasin in self.data_processed:
            cat = magasin.get('categorie_normalisee', 'Autre')
            report['categories'][cat] = report['categories'].get(cat, 0) + 1
        
        # Sauvegarder le rapport
        with open('output/report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info("Rapport d'exécution généré")
        return report


def main():
    """Fonction principale - exemple d'utilisation"""
    logger.info("=" * 50)
    logger.info("Démarrage du scraper")
    logger.info("=" * 50)
    
    # Créer une instance du scraper
    scraper = CentrCommercialScraper()
    
    # Exemple: scraper un site (à adapter selon votre URL)
    # url = "https://www.centre-commercial.fr/labege2/boutiques/"
    # selectors = {
    #     'container': 'div.magasin',
    #     'nom': 'h3.magasin-nom',
    #     'categorie': 'span.magasin-categorie'
    # }
    # 
    # html = scraper.fetch_page(url)
    # if html:
    #     magasins_bruts = scraper.parse_static(html, url, selectors)
    #     magasins_traites = scraper.process_data(magasins_bruts)
    #     scraper.export_csv()
    #     scraper.export_json()
    #     scraper.generate_report()
    
    logger.info("=" * 50)
    logger.info("Scraping terminé")
    logger.info("=" * 50)


if __name__ == '__main__':
    main()
