"""
Tests unitaires pour le scraper
"""
import unittest
import sys
sys.path.insert(0, '../scripts')

from parser import MagasinParser
from utils import validate_magasin_data


class TestMagasinParser(unittest.TestCase):
    """Tests pour le parser de magasins"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.html_example = """
        <div class="magasin">
            <h3>Zara</h3>
            <span class="category">Mode</span>
            <p class="horaires">9h-20h</p>
        </div>
        <div class="magasin">
            <h3>Décathlon</h3>
            <span class="category">Sport</span>
            <p class="horaires">9h-22h</p>
        </div>
        """
    
    def test_parse_magasins(self):
        """Test l'extraction des magasins"""
        parser = MagasinParser(self.html_example, "http://example.com")
        selectors = {
            'container': 'div.magasin',
            'nom': 'h3',
            'categorie': '.category',
            'horaires': '.horaires'
        }
        
        magasins = parser.parse_generic(selectors)
        
        self.assertEqual(len(magasins), 2)
        self.assertEqual(magasins[0]['nom'], 'Zara')
        self.assertEqual(magasins[1]['nom'], 'Décathlon')
    
    def test_validate_magasin_data(self):
        """Test la validation des données"""
        valid_magasin = {'nom': 'Zara', 'categorie': 'Mode'}
        invalid_magasin = {'nom': 'Zara'}
        
        self.assertTrue(validate_magasin_data(valid_magasin))
        self.assertFalse(validate_magasin_data(invalid_magasin))
    
    def test_source_tracking(self):
        """Test que la source est bien tracée"""
        parser = MagasinParser(self.html_example, "http://example.com")
        selectors = {
            'container': 'div.magasin',
            'nom': 'h3',
            'categorie': '.category'
        }
        
        magasins = parser.parse_generic(selectors)
        
        for magasin in magasins:
            self.assertEqual(magasin['source_url'], "http://example.com")
            self.assertIn('extraction_id', magasin)


class TestDataValidation(unittest.TestCase):
    """Tests pour la validation des données"""
    
    def test_empty_magasin(self):
        """Test avec un magasin vide"""
        self.assertFalse(validate_magasin_data({}))
    
    def test_null_values(self):
        """Test avec des valeurs nulles"""
        magasin = {'nom': None, 'categorie': 'Mode'}
        self.assertFalse(validate_magasin_data(magasin))
    
    def test_valid_magasin(self):
        """Test avec un magasin valide"""
        magasin = {
            'nom': 'Test Store',
            'categorie': 'Test Category',
            'horaires': '9h-20h'
        }
        self.assertTrue(validate_magasin_data(magasin))


if __name__ == '__main__':
    unittest.main()
