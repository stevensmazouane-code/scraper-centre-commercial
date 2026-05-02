"""
Utilitaires pour le scraping de centres commerciaux
"""
import logging
import json
from datetime import datetime
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def setup_directories():
    """Crée les répertoires nécessaires s'ils n'existent pas"""
    dirs = ['data/raw', 'data/processed', 'output', 'logs']
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
    logger.info("Répertoires configurés")


def save_raw_data(data, filename, source_url):
    """
    Sauvegarde les données brutes avec les informations de source
    
    Args:
        data: Les données brutes (dict ou list)
        filename: Nom du fichier de sortie
        source_url: URL source pour traçabilité
    """
    raw_file = f'data/raw/{filename}'
    
    # Sauvegarder les données
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Sauvegarder les métadonnées (source obligatoire)
    metadata = {
        'source_url': source_url,
        'timestamp': datetime.now().isoformat(),
        'filename': filename,
        'record_count': len(data) if isinstance(data, list) else 1
    }
    
    meta_file = f'data/raw/{filename.replace(".json", "_metadata.json")}'
    with open(meta_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Données brutes sauvegardées: {raw_file}")
    logger.info(f"Métadonnées sauvegardées: {meta_file}")
    
    return raw_file, meta_file


def log_error(error_type, error_message, context=None):
    """
    Log les erreurs de scraping
    
    Args:
        error_type: Type d'erreur (NetworkError, ParsingError, etc)
        error_message: Message d'erreur
        context: Contexte additionnel
    """
    error_log = {
        'timestamp': datetime.now().isoformat(),
        'error_type': error_type,
        'message': error_message,
        'context': context
    }
    
    logger.error(f"{error_type}: {error_message}")
    
    # Sauvegarder dans un fichier d'erreurs
    with open('output/errors.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(error_log, ensure_ascii=False) + '\n')


def validate_magasin_data(magasin):
    """
    Valide les données d'un magasin
    
    Args:
        magasin: Dict contenant les infos du magasin
        
    Returns:
        bool: True si valide, False sinon
    """
    required_fields = ['nom', 'categorie']
    
    if not isinstance(magasin, dict):
        return False
    
    return all(field in magasin and magasin[field] for field in required_fields)


def get_execution_stats():
    """Retourne les stats d'exécution"""
    return {
        'timestamp': datetime.now().isoformat(),
        'status': 'completed'
    }
