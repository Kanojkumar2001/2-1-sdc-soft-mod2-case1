import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.fuzzy_system.inference_system import FuzzyInferenceSystem
from src.fuzzy_system.membership_functions import MembershipFunctions
from src.fuzzy_system.rule_engine import RuleEngine

class TestFuzzySystem(unittest.TestCase):
    
    def setUp(self):
        self.fuzzy_system = FuzzyInferenceSystem()
        self.membership = MembershipFunctions()
        self.rule_engine = RuleEngine()
    
    def test_membership_functions(self):
        """Test membership function values"""
        # Test triangular
        x = 5
        result = self.membership.triangular(x, 0, 5, 10)
        self.assertEqual(result, 1.0)
        
        # Test trapezoidal
        x = 7.5
        result = self.membership.trapezoidal(x, 0, 5, 10, 15)
        self.assertEqual(result, 1.0)
    
    def test_rule_engine(self):
        """Test rule engine functionality"""
        rules = self.rule_engine.get_rules()
        self.assertGreater(len(rules), 0)
        
        # Test rule structure
        for rule in rules:
            self.assertIn('if', rule)
            self.assertIn('then', rule)
    
    def test_fuzzification(self):
        """Test fuzzification process"""
        # Test income fuzzification
        income_value = 45000
        fuzzified = self.fuzzy_system.fuzzify('income', income_value)
        
        self.assertIn('low', fuzzified)
        self.assertIn('medium', fuzzified)
        self.assertIn('high', fuzzified)
        
        # Check that values are between 0 and 1
        for value in fuzzified.values():
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 1)
    
    def test_classification(self):
        """Test behavior classification"""
        test_data = {
            'income': 45000,
            'expenses': 30000,
            'savings': 10000,
            'debt': 5000,
            'risk_tolerance': 6
        }
        
        result = self.fuzzy_system.evaluate(test_data)
        
        self.assertIn('behavior', result)
        self.assertIn('score', result)
        self.assertIn('strategies', result)
        
        # Check that behavior is one of expected categories
        expected_behaviors = ['cautious', 'conservative', 'moderate', 'aggressive']
        self.assertIn(result['behavior'], expected_behaviors)

if __name__ == '__main__':
    unittest.main()