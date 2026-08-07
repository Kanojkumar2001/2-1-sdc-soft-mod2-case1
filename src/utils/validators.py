"""
Input validation utilities
"""

import re
from collections.abc import Mapping
from typing import Dict, Any, Tuple

class InputValidator:
    """Validates user financial data inputs"""
    
    def __init__(self):
        self.required_fields = [
            'income', 'expenses', 'savings', 'debt', 'risk_tolerance'
        ]
        self.optional_fields = [
            'user_id', 'age', 'employment_status', 'dependents',
            'financial_goals', 'investment_knowledge'
        ]
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> Tuple[bool, list]:
        """Validate user financial data"""
        errors = []

        if not isinstance(user_data, Mapping):
            errors.append("User data must be a dictionary")
            return False, errors
        
        # Check required fields
        for field in self.required_fields:
            if field not in user_data:
                errors.append(f"Missing required field: {field}")
            else:
                if not self._validate_numeric(user_data[field], field):
                    errors.append(f"Invalid value for {field}: must be numeric and non-negative")
        
        # Validate optional fields
        if 'risk_tolerance' in user_data:
            if not (1 <= user_data['risk_tolerance'] <= 10):
                errors.append("risk_tolerance must be between 1 and 10")
        
        if 'age' in user_data:
            if not (18 <= user_data['age'] <= 100):
                errors.append("age must be between 18 and 100")
        
        if 'income' in user_data and 'expenses' in user_data:
            if user_data['expenses'] > user_data['income']:
                errors.append("Expenses exceed income - check your budget")
        
        return len(errors) == 0, errors
    
    def _validate_numeric(self, value, field_name):
        """Validate numeric field"""
        try:
            val = float(value)
            return val >= 0
        except (ValueError, TypeError):
            return False
    
    def validate_income(self, income):
        """Validate income value"""
        return income >= 0 and income <= 1000000
    
    def validate_risk_score(self, score):
        """Validate risk tolerance score"""
        return 1 <= score <= 10
    
    def validate_employment_status(self, status):
        """Validate employment status"""
        valid_statuses = ['employed', 'self_employed', 'student', 'retired', 'unemployed']
        return status in valid_statuses if status else True
    
    def validate_financial_goal(self, goal):
        """Validate financial goal"""
        valid_goals = [
            'retirement', 'wealth_building', 'debt_reduction',
            'house_purchase', 'emergency_fund', 'children_education'
        ]
        return goal in valid_goals if goal else True