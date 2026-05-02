# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

## [1.0.0] - 2024-01-15

### ✨ Ajouté
- Scraper générique pour sites statiques (BeautifulSoup)
- Support des sites dynamiques avec Selenium
- Parser flexible avec sélecteurs CSS personnalisables
- Classification automatique des catégories de magasins
- Export en CSV et JSON
- Logging détaillé et gestion d'erreurs
- Validation des données
- Extraction obligatoire des sources
- Tests unitaires
- Documentation complète

### 📦 Dépendances
- beautifulsoup4 4.12.2
- requests 2.31.0
- selenium 4.15.2
- pandas 2.1.3
- python-dotenv 1.0.0
- lxml 4.9.3

### 🔒 Sécurité
- Respect du robots.txt
- User-Agent approprié
- Gestion des erreurs de requête
- Logging des sources pour traçabilité

## Format de version

Ce projet suit [Semantic Versioning](https://semver.org/lang/fr/).

Les versions sont formatées comme `MAJOR.MINOR.PATCH` :
- **MAJOR**: Changements incompatibles avec les versions précédentes
- **MINOR**: Nouvelles fonctionnalités compatibles avec les versions précédentes
- **PATCH**: Corrections de bugs
