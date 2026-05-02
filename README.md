\# Scraper Centre Commercial



Projet d'atelier collecte de données. Web scraper pour extraire les magasins depuis les sites de centres commerciaux.



\## Description



Le projet consiste à créer un pipeline de scraping qui récupère les données de magasins depuis les sites web de centres commerciaux, les normalise et les exporte en CSV/JSON.



Supports:

\- Sites statiques avec BeautifulSoup

\- Sites dynamiques avec Selenium

\- Gestion des erreurs et logging

\- Export CSV et JSON avec traçabilité des sources



\## Structure

.

├── scripts/

│   ├── scraper.py        # Classe principale

│   ├── parser.py         # Parsing HTML

│   └── utils.py          # Utilitaires

├── data/

│   ├── raw/              # Données brutes

│   └── processed/        # Données traitées

├── output/               # Résultats (CSV, JSON, logs)

├── tests/                # Tests unitaires

├── README.md

├── requirements.txt

└── example.py            # Script d'exemple



\## Installation



Python 3.8+ requis.



```bash

pip install -r requirements.txt

```



\## Utilisation



Lancer l'exemple:

```bash

python example.py

```



Ou utiliser directement:

```python

from scripts.scraper import CentrCommercialScraper



scraper = CentrCommercialScraper()

html = scraper.fetch\_page("https://...")

magasins = scraper.parse\_static(html, url, {

&#x20;   'container': 'div.magasin',

&#x20;   'nom': 'h3',

&#x20;   'categorie': '.type'

})

processed = scraper.process\_data(magasins)

scraper.export\_csv()

scraper.export\_json()

```



\## Données



Sortie en CSV:

nom,categorie,localisation,date\_extraction,categorie\_normalisee

Zara,Vêtements,Étage 1,2024-01-15,Mode

Décathlon,Sport,Étage 0,2024-01-15,Loisirs



Et en JSON avec métadonnées (source, ID extraction, etc).



\## Aspects légaux



\- Respect du robots.txt

\- Respect des CGU du site

\- User-Agent approprié

\- Extraction des sources obligatoire pour traçabilité



\## Tests



```bash

python -m pytest tests/

```



\## Limitations



\- Identification du scraper (User-Agent, IP)

\- Captcha et rate limiting

\- Sites avec protections anti-scraping

\- Modification du design du site

