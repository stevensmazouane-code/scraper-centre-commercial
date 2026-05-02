#!/usr/bin/env python3
"""
Exemple d'utilisation du scraper Centre Commercial
Ce script montre comment scraper un site et exporter les données
"""

import sys
import os

# Ajouter le répertoire scripts au chemin
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from scraper import CentrCommercialScraper


def example_static_scraping():
    """Exemple: scraper un site statique"""
    print("\n" + "="*60)
    print("EXEMPLE 1: Scraper un site STATIQUE")
    print("="*60)
    
    scraper = CentrCommercialScraper()
    
    # Configuration pour un site statique
    url = "https://www.centre-commercial.fr/labege2/boutiques/"
    
    selectors = {
        'container': 'div.magasin',          # Chaque magasin dans une div.magasin
        'nom': 'h3.magasin-nom',             # Nom dans h3 avec classe magasin-nom
        'categorie': 'span.categorie',       # Catégorie dans span.categorie
        'horaires': 'p.horaires',            # Horaires dans p.horaires
        'localisation': 'span.etage'         # Localisation dans span.etage
    }
    
    print(f"\n📍 Scraping: {url}")
    
    # Récupérer la page HTML
    html = scraper.fetch_page(url)
    
    if html:
        # Parser les magasins
        print("🔍 Parsing des magasins...")
        magasins_bruts = scraper.parse_static(html, url, selectors)
        
        # Traiter et normaliser les données
        print("⚙️  Traitement des données...")
        magasins_traites = scraper.process_data(magasins_bruts)
        
        # Exporter en CSV et JSON
        print("💾 Export des données...")
        scraper.export_csv('output/magasins_static.csv')
        scraper.export_json('output/magasins_static.json')
        scraper.generate_report()
        
        print(f"\n✅ Scraping terminé!")
        print(f"   - {len(magasins_traites)} magasins extraits")
        print(f"   - CSV: output/magasins_static.csv")
        print(f"   - JSON: output/magasins_static.json")
        print(f"   - Rapport: output/report.json")
    else:
        print("❌ Erreur: impossible de récupérer la page")


def example_dynamic_scraping():
    """Exemple: scraper un site dynamique (avec JavaScript)"""
    print("\n" + "="*60)
    print("EXEMPLE 2: Scraper un site DYNAMIQUE (JavaScript)")
    print("="*60)
    
    scraper = CentrCommercialScraper()
    
    url = "https://example-dynamic-mall.com/stores"
    
    selectors = {
        'container': 'article.store-card',
        'nom': 'h3.store-name',
        'categorie': '.store-category',
        'horaires': '.store-hours'
    }
    
    print(f"\n📍 Scraping: {url}")
    print("⏳ Chargement du contenu dynamique (Selenium)...")
    
    # Pour un site dynamique, utiliser parse_dynamic
    # Cela utilisera Selenium pour charger le JavaScript
    try:
        magasins_bruts = scraper.parse_dynamic(
            url,
            wait_selector='article.store-card',  # Attendre ce sélecteur
            selectors=selectors
        )
        
        if magasins_bruts:
            magasins_traites = scraper.process_data(magasins_bruts)
            scraper.export_csv('output/magasins_dynamic.csv')
            scraper.export_json('output/magasins_dynamic.json')
            
            print(f"\n✅ Scraping dynamique terminé!")
            print(f"   - {len(magasins_traites)} magasins extraits")
        else:
            print("❌ Aucun magasin trouvé")
    except Exception as e:
        print(f"⚠️  Note: Pour utiliser Selenium, installer: pip install selenium")
        print(f"   Erreur: {str(e)}")


def example_from_config():
    """Exemple: charger la configuration depuis un fichier"""
    print("\n" + "="*60)
    print("EXEMPLE 3: Utiliser un fichier de CONFIGURATION")
    print("="*60)
    
    # Créer d'abord un fichier config.json
    print("📄 Utilisation de config.json...")
    
    try:
        scraper = CentrCommercialScraper(config_file='config.json')
        print("✅ Configuration chargée")
        print("   Sites configurés:")
        for site in scraper.config.get('sites', []):
            print(f"   - {site['nom']} ({site['url']})")
    except FileNotFoundError:
        print("⚠️  Fichier config.json non trouvé")
        print("   Créer: cp config.json.example config.json")


def main():
    """Fonction principale"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "SCRAPER CENTRE COMMERCIAL" + " "*18 + "║")
    print("║" + " "*14 + "Exemples d'utilisation du scraper" + " "*12 + "║")
    print("╚" + "="*58 + "╝")
    
    print("\n📋 Sélectionnez un exemple à exécuter:")
    print("\n1. Scraper un site STATIQUE (BeautifulSoup)")
    print("2. Scraper un site DYNAMIQUE (Selenium)")
    print("3. Charger depuis une CONFIGURATION")
    print("4. Exécuter tous les exemples")
    print("0. Quitter")
    
    choice = input("\nVotre choix (0-4): ").strip()
    
    if choice == "1":
        example_static_scraping()
    elif choice == "2":
        example_dynamic_scraping()
    elif choice == "3":
        example_from_config()
    elif choice == "4":
        example_static_scraping()
        example_dynamic_scraping()
        example_from_config()
    elif choice != "0":
        print("❌ Choix invalide")
    
    if choice in ["1", "2", "3", "4"]:
        print("\n" + "="*60)
        print("📁 Fichiers générés dans le répertoire 'output/'")
        print("="*60)


if __name__ == '__main__':
    main()
