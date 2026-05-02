.PHONY: help install test run clean lint format

help:
	@echo "╔════════════════════════════════════════════════════════╗"
	@echo "║     SCRAPER CENTRE COMMERCIAL - Commandes Utiles       ║"
	@echo "╚════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Commandes disponibles:"
	@echo "  make install      - Installer les dépendances"
	@echo "  make test         - Exécuter les tests"
	@echo "  make run          - Lancer l'exemple interactif"
	@echo "  make clean        - Nettoyer les fichiers générés"
	@echo "  make lint         - Vérifier la qualité du code"
	@echo "  make format       - Formater le code (autopep8)"
	@echo "  make init-git     - Initialiser le repository git"
	@echo ""

install:
	@echo "📦 Installation des dépendances..."
	pip install -r requirements.txt
	@echo "✅ Installation terminée"

test:
	@echo "🧪 Exécution des tests..."
	python -m pytest tests/ -v || python tests/test_scraper.py
	@echo "✅ Tests terminés"

run:
	@echo "🚀 Lancement du scraper..."
	python example.py

example:
	python example.py

clean:
	@echo "🧹 Nettoyage..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/
	rm -f scraping.log
	@echo "✅ Nettoyage terminé"

lint:
	@echo "🔍 Vérification du code..."
	python -m pylint scripts/*.py tests/*.py 2>/dev/null || echo "pylint non installé"
	python -m flake8 scripts/ tests/ 2>/dev/null || echo "flake8 non installé"
	@echo "✅ Vérification terminée"

format:
	@echo "📝 Formatage du code..."
	python -m autopep8 --in-place --aggressive scripts/*.py
	python -m autopep8 --in-place --aggressive tests/*.py
	@echo "✅ Formatage terminé"

init-git:
	@echo "📦 Initialisation du repository Git..."
	git init
	git add .
	git commit -m "Initial commit - Scraper Centre Commercial v1.0.0"
	@echo "✅ Repository Git initialisé"
	@echo ""
	@echo "Prochaines étapes:"
	@echo "  git remote add origin <votre-repo-url>"
	@echo "  git branch -M main"
	@echo "  git push -u origin main"

.DEFAULT_GOAL := help
