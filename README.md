# 🏪 Scraper Centre Commercial

Pipeline automatisé d'ingestion de données pour centres commerciaux européens avec suivi des magasins et historique des ouvertures/fermetures.

## 📋 Vue d'ensemble

Ce projet fournit une solution complète de **web scraping** pour extraire et structurer les données de magasins depuis les sites de centres commerciaux. 

**Livrables :**
- ✅ Base de données exploitable des centres commerciaux et magasins associés
- ✅ Classification des magasins par catégorie
- ✅ Dates d'ouverture et fermeture
- ✅ Données en format CSV et JSON
- ✅ Code source reproductible
- ✅ Extraction des sources obligatoire
- ✅ Séparation des étapes (données brutes vs traitées)
- ✅ Gestion complète des erreurs de scraping

## 🚀 Fonctionnalités

### Scraping
- Support des sites **statiques** (HTML simple) avec BeautifulSoup
- Support des sites **dynamiques** (JavaScript) avec Selenium
- Sélecteurs CSS personnalisables pour chaque site
- Gestion des erreurs réseau et timeouts
- Logging détaillé de toutes les opérations

### Traitement des données
- Normalisation des données brutes
- Classification automatique des catégories
- Validation des données
- Extraction obligatoire des sources
- Séparation données brutes / traitées

### Exportation
- Format CSV (exploitable dans Excel, SQL, etc.)
- Format JSON (structure complète avec métadonnées)
- Rapport d'exécution automatique
- Suivi des erreurs en JSONL

## 📂 Structure du projet

```
scraper-centre-commercial/
├── README.md                 # Documentation
├── requirements.txt          # Dépendances Python
├── config.json.example       # Configuration d'exemple
├── .gitignore               # Fichiers à ignorer
│
├── scripts/
│   ├── scraper.py          # Script principal de scraping
│   ├── parser.py           # Parsers (static/dynamic)
│   └── utils.py            # Utilitaires et logging
│
├── data/
│   ├── raw/                # Données brutes + métadonnées
│   │   ├── magasins_raw.json
│   │   └── magasins_raw_metadata.json
│   └── processed/          # Données nettoyées
│
├── output/                 # Résultats finaux
│   ├── magasins.csv       # Export CSV principal
│   ├── magasins.json      # Export JSON
│   ├── report.json        # Rapport d'exécution
│   └── errors.jsonl       # Log des erreurs
│
└── tests/
    └── test_scraper.py     # Tests unitaires
```

## 🔧 Installation

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Étapes

1. **Cloner le repository**
```bash
git clone <votre-repo>
cd scraper-centre-commercial
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration (optionnel)**
```bash
cp config.json.example config.json
# Éditer config.json avec vos URLs et sélecteurs
```

## 💻 Utilisation

### Cas 1: Scraper un site statique

```python
from scripts.scraper import CentrCommercialScraper

scraper = CentrCommercialScraper()

url = "https://www.centre-commercial.fr/labege2/boutiques/"
selectors = {
    'container': 'div.magasin',        # Conteneur de chaque magasin
    'nom': 'h3.magasin-nom',           # Sélecteur du nom
    'categorie': 'span.magasin-cat',   # Sélecteur de la catégorie
    'horaires': 'p.horaires',          # Optionnel
    'localisation': 'span.localisation' # Optionnel
}

# Récupérer la page
html = scraper.fetch_page(url)

# Parser les magasins
magasins_bruts = scraper.parse_static(html, url, selectors)

# Traiter les données
magasins_traites = scraper.process_data(magasins_bruts)

# Exporter
scraper.export_csv()    # → output/magasins.csv
scraper.export_json()   # → output/magasins.json
scraper.generate_report() # → output/report.json
```

### Cas 2: Scraper un site dynamique

```python
scraper = CentrCommercialScraper()

url = "https://example-shopping-mall.com/stores"
selectors = {
    'container': 'article.store',
    'nom': 'h2',
    'categorie': '.category'
}

# Parser avec Selenium (attendre le chargement du JS)
magasins = scraper.parse_dynamic(
    url, 
    wait_selector='article.store',  # Attendre ce sélecteur
    selectors=selectors
)

magasins_traites = scraper.process_data(magasins)
scraper.export_csv()
```

### Cas 3: Utiliser un fichier de configuration

```python
scraper = CentrCommercialScraper(config_file='config.json')
# Les configurations sont chargées depuis le fichier
```

## 📊 Format des données

### CSV (output/magasins.csv)
```csv
nom,categorie,localisation,horaires,date_extraction,categorie_normalisee
Zara,Vêtements & Mode,Étage 1,9h-20h,2024-01-15,Mode
Décathlon,Sport & Loisirs,Étage 0,9h-22h,2024-01-15,Loisirs
```

### JSON (output/magasins.json)
```json
[
  {
    "nom": "Zara",
    "categorie": "Vêtements & Mode",
    "categorie_normalisee": "Mode",
    "localisation": "Étage 1",
    "horaires": "9h-20h",
    "date_extraction": "2024-01-15",
    "source_url": "https://...",
    "extraction_id": "1"
  }
]
```

### Rapport (output/report.json)
```json
{
  "execution_stats": {
    "timestamp": "2024-01-15T14:30:00",
    "status": "completed"
  },
  "total_magasins": 127,
  "categories": {
    "Mode": 35,
    "Électronique": 12,
    "Hyper/Supermarché": 8,
    "Loisirs": 22
  }
}
```

## ⚠️ Aspects Légaux

### Respect des bonnes pratiques
- ✅ Respect du `robots.txt` du site
- ✅ Respect des CGU/Conditions d'utilisation
- ✅ Respect du droit d'auteur (données publiques)
- ✅ Extraction obligatoire des sources (traçabilité)
- ✅ Limitation des requêtes (délais entre requêtes)
- ✅ User-Agent approprié

### Points importants
- Vérifier les CGU du site avant scraping
- Respecter les délais entre requêtes
- Ne pas surcharger les serveurs
- Inclure les sources dans les données

## 🚨 Limitations et gestion d'erreurs

### Limitations courantes
1. **Identification de la machine**
   - User-Agent détecté
   - Adresse IP bloquée
   - Croisement de signatures (navigateur, IP, langue)

2. **Obstacles techniques**
   - Captcha
   - Rate limiting
   - Blocage par proxy/firewall

3. **Instabilités du scraping**
   - Modification du site (design, classe CSS)
   - Erreur coté scraper (bug, connexion)
   - Erreur coté serveur (timeout, indisponibilité)

### Gestion des erreurs
Tous les erreurs sont loggées dans `output/errors.jsonl` :
```json
{
  "timestamp": "2024-01-15T14:30:00",
  "error_type": "NetworkError",
  "message": "Timeout lors de la récupération",
  "context": {"url": "https://..."}
}
```

## 🧪 Tests

```bash
# Exécuter les tests
python -m pytest tests/

# Ou avec unittest
python tests/test_scraper.py
```

## 🔍 Débogage

### Activer le logging verbeux
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Fichiers de log
- `scraping.log` - Log complet d'exécution
- `output/errors.jsonl` - Erreurs structurées

## 📦 Dépendances

- **beautifulsoup4** - Parsing HTML
- **requests** - Récupération des pages (statique)
- **selenium** - Automation browser (dynamique)
- **pandas** - Manipulation et export CSV
- **python-dotenv** - Configuration par variables d'env
- **lxml** - Parser HTML performant

Installer: `pip install -r requirements.txt`

## 📝 Exemple complet

```bash
# 1. Cloner et installer
git clone <repo>
cd scraper-centre-commercial
pip install -r requirements.txt

# 2. Créer un script de scraping
cat > main.py << 'EOF'
from scripts.scraper import CentrCommercialScraper

scraper = CentrCommercialScraper()

# Configuration des sélecteurs
url = "https://votre-site.com/boutiques"
selectors = {
    'container': 'div.magasin',
    'nom': 'h3',
    'categorie': '.type'
}

# Scraper
html = scraper.fetch_page(url)
magasins = scraper.parse_static(html, url, selectors)
processed = scraper.process_data(magasins)

# Exporter
scraper.export_csv()
scraper.export_json()
scraper.generate_report()

print(f"✅ {len(processed)} magasins extraits")
EOF

# 3. Exécuter
python main.py

# 4. Vérifier les résultats
ls -la output/
cat output/report.json
```

## 📄 Licence

Propriétaire - Usage éducationnel et commercial avec respect des CGU

## 👥 Auteur

Atelier Collecte de Données - EPSI

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :
1. Fork le repository
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

**Status** : Production-ready | **Dernière mise à jour** : Janvier 2024
