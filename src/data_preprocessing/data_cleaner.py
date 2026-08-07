"""
Data cleaning and preprocessing module
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

class DataCleaner:
    """Handles cleaning and preprocessing of financial data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def clean_single_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a single user's data"""
        cleaned_data = user_data.copy()
        
        # Ensure required fields
        required_fields = ['income', 'expenses', 'savings', 'debt', 'risk_tolerance']
        for field in required_fields:
            if field not in cleaned_data:
                cleaned_data[field] = 0
            elif pd.isna(cleaned_data[field]):
                cleaned_data[field] = 0
        
        # Ensure positive values
        cleaned_data['income'] = max(0, cleaned_data['income'])
        cleaned_data['expenses'] = max(0, cleaned_data['expenses'])
        cleaned_data['savings'] = max(0, cleaned_data['savings'])
        cleaned_data['debt'] = max(0, cleaned_data['debt'])
        
        # Clip risk tolerance to 1-10 range
        cleaned_data['risk_tolerance'] = max(1, min(10, cleaned_data['risk_tolerance']))
        
        # Calculate derived features
        cleaned_data['savings_ratio'] = cleaned_data['savings'] / (cleaned_data['income'] + 1)
        cleaned_data['expense_ratio'] = cleaned_data['expenses'] / (cleaned_data['income'] + 1)
        cleaned_data['debt_to_income'] = cleaned_data['debt'] / (cleaned_data['income'] + 1)
        cleaned_data['disposable_income'] = cleaned_data['income'] - cleaned_data['expenses']
        
        return cleaned_data
    
    def clean_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean a batch of user data"""
        cleaned_dfs = []
        
        for _, row in df.iterrows():
            cleaned_user = self.clean_single_user(row.to_dict())
            cleaned_dfs.append(cleaned_user)
        
        cleaned_df = pd.DataFrame(cleaned_dfs)
        self.logger.info(f"Cleaned {len(cleaned_df)} records")
        
        return cleaned_df
    
    def normalize_data(self, df: pd.DataFrame, method='min_max') -> pd.DataFrame:
        """Normalize numerical columns"""
        numerical_cols = ['income', 'expenses', 'savings', 'debt', 'risk_tolerance']
        
        if method == 'min_max':
            for col in numerical_cols:
                if col in df.columns:
                    min_val = df[col].min()
                    max_val = df[col].max()
                    if max_val > min_val:
                        df[f'{col}_normalized'] = (df[col] - min_val) / (max_val - min_val)
                    else:
                        df[f'{col}_normalized'] = 0.5
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy='mean') -> pd.DataFrame:
        """Handle missing values in the dataset"""
        if strategy == 'mean':
            return df.fillna(df.mean(numeric_only=True))
        elif strategy == 'median':
            return df.fillna(df.median(numeric_only=True))
        elif strategy == 'zero':
            return df.fillna(0)
        else:
            return df.dropna()