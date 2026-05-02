"""
Parser pour extraire les données de magasins depuis l'HTML
"""
from bs4 import BeautifulSoup
import logging
import json
from utils import validate_magasin_data, log_error

logger = logging.getLogger(__name__)


class MagasinParser:
    """
    Parser générique pour extraire les données de magasins
    depuis des pages HTML de centres commerciaux
    """
    
    def __init__(self, html_content, source_url):
        """
        Initialise le parser
        
        Args:
            html_content: Contenu HTML à parser
            source_url: URL source pour traçabilité
        """
        self.html = html_content
        self.source_url = source_url
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.magasins = []
        self.errors = []
        
    def parse_generic(self, selectors):
        """
        Parse les magasins avec des sélecteurs CSS personnalisés
        
        Args:
            selectors: Dict contenant les sélecteurs CSS
                - container: Sélecteur pour chaque magasin
                - nom: Sélecteur pour le nom du magasin
                - categorie: Sélecteur pour la catégorie
                - horaires: Sélecteur pour les horaires (optionnel)
                
        Returns:
            list: Liste des magasins parsés
        """
        try:
            containers = self.soup.select(selectors.get('container', 'div.magasin'))
            logger.info(f"Trouvé {len(containers)} conteneurs de magasins")
            
            for i, container in enumerate(containers):
                try:
                    magasin = self._extract_magasin(container, selectors)
                    
                    if validate_magasin_data(magasin):
                        magasin['source_url'] = self.source_url
                        magasin['extraction_id'] = f"{i+1}"
                        self.magasins.append(magasin)
                    else:
                        self.errors.append({
                            'index': i,
                            'reason': 'Données invalides',
                            'data': magasin
                        })
                        
                except Exception as e:
                    self.errors.append({
                        'index': i,
                        'reason': str(e),
                        'data': None
                    })
                    log_error('ParsingError', f"Erreur lors du parsing du magasin {i}", 
                             {'container_index': i})
            
            logger.info(f"Extraction réussie: {len(self.magasins)} magasins, "
                       f"{len(self.errors)} erreurs")
            
        except Exception as e:
            log_error('ParsingError', f"Erreur générale du parsing: {str(e)}")
            raise
        
        return self.magasins
    
    def _extract_magasin(self, container, selectors):
        """
        Extrait les informations d'un magasin d'un conteneur HTML
        
        Args:
            container: Élément BeautifulSoup du magasin
            selectors: Dict des sélecteurs CSS
            
        Returns:
            dict: Informations du magasin
        """
        magasin = {}
        
        # Nom
        nom_elem = container.select_one(selectors.get('nom', 'h2, h3'))
        magasin['nom'] = nom_elem.get_text(strip=True) if nom_elem else None
        
        # Catégorie
        cat_elem = container.select_one(selectors.get('categorie', '.category, .type'))
        magasin['categorie'] = cat_elem.get_text(strip=True) if cat_elem else 'Non spécifiée'
        
        # Horaires (optionnel)
        if 'horaires' in selectors:
            horaires_elem = container.select_one(selectors.get('horaires'))
            magasin['horaires'] = horaires_elem.get_text(strip=True) if horaires_elem else None
        
        # Étage/localisation (optionnel)
        if 'localisation' in selectors:
            loc_elem = container.select_one(selectors.get('localisation'))
            magasin['localisation'] = loc_elem.get_text(strip=True) if loc_elem else None
        
        return magasin
    
    def get_magasins(self):
        """Retourne les magasins extraits"""
        return self.magasins
    
    def get_errors(self):
        """Retourne les erreurs d'extraction"""
        return self.errors
    
    def export_json(self, filename):
        """Exporte les magasins en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.magasins, f, ensure_ascii=False, indent=2)
        logger.info(f"Données exportées en JSON: {filename}")


class StaticParser(MagasinParser):
    """Parser pour sites statiques (HTML simple)"""
    pass


class DynamicParser(MagasinParser):
    """
    Parser pour sites dynamiques (JavaScript)
    Nécessite Selenium pour charger le contenu dynamique
    """
    
    @staticmethod
    def parse_with_selenium(url, wait_selector=None):
        """
        Parse un site dynamique avec Selenium
        
        Args:
            url: URL du site
            wait_selector: Sélecteur à attendre avant le parsing
            
        Returns:
            str: Contenu HTML rendu
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # Attendre le chargement du contenu
            if wait_selector:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, wait_selector))
                )
            
            html = driver.page_source
            driver.quit()
            
            return html
            
        except Exception as e:
            log_error('SeleniumError', f"Erreur Selenium: {str(e)}", 
                     {'url': url})
            raise
