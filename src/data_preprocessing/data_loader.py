"""
Data loader module for reading financial data
"""

import pandas as pd
import logging
from pathlib import Path

class DataLoader:
    """Handles loading of financial data from various sources"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_csv(self, file_path):
        """Load data from CSV file"""
        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading CSV: {str(e)}")
            raise
    
    def load_excel(self, file_path):
        """Load data from Excel file"""
        try:
            df = pd.read_excel(file_path)
            self.logger.info(f"Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading Excel: {str(e)}")
            raise
    
    def load_json(self, file_path):
        """Load data from JSON file"""
        try:
            df = pd.read_json(file_path)
            self.logger.info(f"Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading JSON: {str(e)}")
            raise
    
    def load_sample_data(self):
        """Load sample user data for testing"""
        sample_data = {
            'user_id': [1, 2, 3],
            'age': [25, 34, 42],
            'income': [32000, 45000, 38000],
            'expenses': [21000, 28000, 35000],
            'savings': [8000, 12000, 2000],
            'debt': [5000, 15000, 25000],
            'risk_tolerance': [6, 8, 3],
            'investment_knowledge': [4, 7, 5]
        }
        return pd.DataFrame(sample_data)