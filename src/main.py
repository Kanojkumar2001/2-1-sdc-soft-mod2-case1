"""
Main entry point for the Personal Finance Advisor System
"""

import sys
import logging
from pathlib import Path
import yaml
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add src to path
sys.path.append(str(PROJECT_ROOT))

from src.data_preprocessing.data_loader import DataLoader
from src.data_preprocessing.data_cleaner import DataCleaner
from src.fuzzy_system.inference_system import FuzzyInferenceSystem
from src.models.fuzzy_classifier import FuzzyClassifier
from src.models.strategy_recommender import StrategyRecommender
from src.utils.validators import InputValidator
from src.utils.helpers import setup_logging

class FinanceAdvisor:
    """Main class for the Personal Finance Advisor System"""
    
    def __init__(self, config_path="config/config.yaml"):
        """Initialize the finance advisor system"""
        self.logger = setup_logging()
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.data_loader = DataLoader()
        self.data_cleaner = DataCleaner()
        self.fuzzy_system = FuzzyInferenceSystem(self.config)
        self.classifier = FuzzyClassifier(self.fuzzy_system)
        self.recommender = StrategyRecommender(self.fuzzy_system)
        self.validator = InputValidator()
        
        self.logger.info("Finance Advisor System initialized successfully")
    
    def _load_config(self, config_path):
        """Load configuration from YAML file"""
        config_path = self._resolve_path(config_path)
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def _resolve_path(self, path):
        """Resolve a path relative to the project root."""
        if not path:
            return PROJECT_ROOT / 'config' / 'config.yaml'

        path_obj = Path(path)
        if path_obj.is_absolute():
            return path_obj

        for base in [PROJECT_ROOT, Path.cwd()]:
            candidate = base / path_obj
            if candidate.exists():
                return candidate

        return PROJECT_ROOT / path_obj
    
    def process_user_data(self, user_data):
        """Process a single user's financial data"""
        try:
            # Validate input
            is_valid, errors = self.validator.validate_user_data(user_data)
            if not is_valid:
                raise ValueError(f"Invalid user data: {errors}")
            
            # Clean data
            cleaned_data = self.data_cleaner.clean_single_user(user_data)
            
            # Classify behavior using fuzzy logic
            behavior = self.classifier.classify(cleaned_data)
            
            # Get strategy recommendations
            strategies = self.recommender.recommend(behavior, cleaned_data)
            
            # Generate report
            report = {
                'user_id': user_data.get('user_id', 'unknown'),
                'behavior_category': behavior,
                'recommended_strategies': strategies,
                'risk_score': self._calculate_risk_score(cleaned_data),
                'financial_health_score': self._calculate_health_score(cleaned_data)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error processing user data: {str(e)}")
            raise
    
    def process_batch_data(self, file_path):
        """Process multiple users from a CSV file"""
        try:
            # Load data
            df = self.data_loader.load_csv(file_path)
            
            # Clean data
            cleaned_df = self.data_cleaner.clean_batch(df)
            
            # Process each user
            reports = []
            for _, row in cleaned_df.iterrows():
                user_data = row.to_dict()
                report = self.process_user_data(user_data)
                reports.append(report)
            
            # Save reports
            report_df = pd.DataFrame(reports)
            output_path = PROJECT_ROOT / 'outputs' / 'reports' / 'financial_advice_report.csv'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            report_df.to_csv(output_path, index=False)
            
            self.logger.info(f"Processed {len(reports)} users successfully")
            return reports
            
        except Exception as e:
            self.logger.error(f"Error processing batch data: {str(e)}")
            raise
    
    def _calculate_risk_score(self, user_data):
        """Calculate overall risk score"""
        income = user_data.get('income', 0)
        savings = user_data.get('savings', 0)
        debt = user_data.get('debt', 0)
        risk_tolerance = user_data.get('risk_tolerance', 5)
        
        # Simple risk calculation
        debt_ratio = debt / (income + 1)  # Avoid division by zero
        savings_ratio = savings / (income + 1)
        
        risk_score = (risk_tolerance / 10) * 0.4 + \
                    (1 - debt_ratio) * 0.3 + \
                    savings_ratio * 0.3
        
        return min(max(risk_score * 100, 0), 100)
    
    def _calculate_health_score(self, user_data):
        """Calculate financial health score"""
        income = user_data.get('income', 0)
        expenses = user_data.get('expenses', 0)
        savings = user_data.get('savings', 0)
        debt = user_data.get('debt', 0)
        
        # Financial health indicators
        saving_rate = savings / (income + 1)
        expense_rate = expenses / (income + 1)
        debt_ratio = debt / (income + 1)
        
        health_score = (saving_rate * 0.4) + \
                      (1 - expense_rate) * 0.3 + \
                      (1 - debt_ratio) * 0.3
        
        return min(max(health_score * 100, 0), 100)

def main():
    """Main function to run the advisor system"""
    # Initialize system
    advisor = FinanceAdvisor()
    
    # Test with sample user
    sample_user = {
        'user_id': 51,
        'age': 35,
        'income': 45000,
        'expenses': 28000,
        'savings': 12000,
        'debt': 8000,
        'risk_tolerance': 6,
        'investment_knowledge': 5,
        'financial_goals': 'wealth_building',
        'employment_status': 'employed',
        'dependents': 2
    }
    
    # Process user
    report = advisor.process_user_data(sample_user)
    
    print("\n" + "="*60)
    print("PERSONAL FINANCE ADVISOR - RECOMMENDATION REPORT")
    print("="*60)
    print(f"User ID: {report['user_id']}")
    print(f"Behavior Category: {report['behavior_category']}")
    print(f"Risk Score: {report['risk_score']:.2f}/100")
    print(f"Financial Health Score: {report['financial_health_score']:.2f}/100")
    print("\nRecommended Strategies:")
    for strategy in report['recommended_strategies']:
        print(f"  • {strategy}")
    print("="*60 + "\n")
    
    # Process batch data (optional)
    # advisor.process_batch_data('data/raw/user_data_sample.csv')

if __name__ == "__main__":
    main()