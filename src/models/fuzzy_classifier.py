"""
Fuzzy classifier for financial behavior categorization
"""

import logging
from typing import Dict, Any

class FuzzyClassifier:
    """Classifies financial behavior using fuzzy logic"""
    
    def __init__(self, fuzzy_system):
        self.fuzzy_system = fuzzy_system
        self.logger = logging.getLogger(__name__)
    
    def classify(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify user's financial behavior"""
        try:
            result = self.fuzzy_system.evaluate(user_data)
            
            # Add additional classification details
            result['detailed'] = self._get_detailed_analysis(user_data, result)
            
            self.logger.info(f"Classified user {user_data.get('user_id', 'unknown')} as {result['behavior']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Classification error: {str(e)}")
            return {
                'behavior': 'unknown',
                'score': 50,
                'strategies': ['budget_planning'],
                'error': str(e)
            }
    
    def _get_detailed_analysis(self, user_data, result):
        """Provide detailed analysis of classification"""
        analysis = {
            'income_category': self._categorize_income(user_data.get('income', 0)),
            'savings_ratio': user_data.get('savings', 0) / (user_data.get('income', 1) + 1),
            'debt_ratio': user_data.get('debt', 0) / (user_data.get('income', 1) + 1),
            'expense_ratio': user_data.get('expenses', 0) / (user_data.get('income', 1) + 1),
            'risk_score': user_data.get('risk_tolerance', 5) / 10
        }
        
        # Add financial health indicators
        analysis['financial_health'] = 'good' if (
            analysis['savings_ratio'] > 0.2 and 
            analysis['debt_ratio'] < 0.3 and 
            analysis['expense_ratio'] < 0.6
        ) else 'needs_improvement'
        
        return analysis
    
    def _categorize_income(self, income):
        """Categorize income level"""
        if income < 25000:
            return 'low'
        elif income < 50000:
            return 'medium'
        else:
            return 'high'