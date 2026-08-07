"""
Rule engine for fuzzy inference system
"""

import json
import logging
from typing import Dict, List, Any

class RuleEngine:
    """Manages fuzzy rules and inference"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rules = []
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load default fuzzy rules"""
        self.rules = [
            # Income & Savings based rules
            {
                'if': {'income': 'high', 'savings': 'high', 'risk_tolerance': 'high'},
                'then': {'behavior': 'aggressive', 'strategy': 'investment_optimization'},
                'weight': 1.0
            },
            {
                'if': {'income': 'high', 'savings': 'medium', 'risk_tolerance': 'medium'},
                'then': {'behavior': 'moderate', 'strategy': 'wealth_building'},
                'weight': 0.9
            },
            {
                'if': {'income': 'medium', 'savings': 'low', 'debt': 'high'},
                'then': {'behavior': 'cautious', 'strategy': 'debt_management'},
                'weight': 1.0
            },
            {
                'if': {'income': 'low', 'expenses': 'high', 'savings': 'low'},
                'then': {'behavior': 'cautious', 'strategy': 'budget_planning'},
                'weight': 1.0
            },
            {
                'if': {'income': 'medium', 'savings': 'medium', 'debt': 'low'},
                'then': {'behavior': 'moderate', 'strategy': 'emergency_fund_building'},
                'weight': 0.8
            },
            {
                'if': {'income': 'high', 'savings': 'high', 'debt': 'low'},
                'then': {'behavior': 'aggressive', 'strategy': 'retirement_planning'},
                'weight': 0.9
            },
            {
                'if': {'income': 'medium', 'debt': 'high', 'risk_tolerance': 'low'},
                'then': {'behavior': 'conservative', 'strategy': 'risk_management'},
                'weight': 0.9
            },
            {
                'if': {'income': 'low', 'savings': 'medium', 'debt': 'low'},
                'then': {'behavior': 'moderate', 'strategy': 'budget_planning'},
                'weight': 0.7
            },
            {
                'if': {'income': 'high', 'expenses': 'low', 'savings': 'high'},
                'then': {'behavior': 'aggressive', 'strategy': 'wealth_building'},
                'weight': 0.8
            },
            {
                'if': {'income': 'low', 'debt': 'high', 'expenses': 'high'},
                'then': {'behavior': 'cautious', 'strategy': 'debt_management'},
                'weight': 1.0
            }
        ]
        
        self.logger.info(f"Loaded {len(self.rules)} fuzzy rules")
    
    def load_rules_from_file(self, file_path):
        """Load rules from JSON file"""
        try:
            with open(file_path, 'r') as f:
                self.rules = json.load(f)
            self.logger.info(f"Loaded {len(self.rules)} rules from {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading rules: {str(e)}")
            raise
    
    def add_rule(self, rule: Dict[str, Any]):
        """Add a new rule to the engine"""
        self.rules.append(rule)
        self.logger.info(f"Added new rule: {rule}")
    
    def get_rules(self):
        """Get all rules"""
        return self.rules