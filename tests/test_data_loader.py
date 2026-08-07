import unittest
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_preprocessing.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        self.loader = DataLoader()
    
    def test_load_sample_data(self):
        """Test loading sample data"""
        df = self.loader.load_sample_data()
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertIn('income', df.columns)
        self.assertIn('expenses', df.columns)

if __name__ == '__main__':
    unittest.main()