"""
Fuzzy inference system for financial behavior classification
"""

import numpy as np
import logging
from typing import Dict, Any, Tuple
from .membership_functions import MembershipFunctions
from .rule_engine import RuleEngine

class FuzzyInferenceSystem:
    """Main fuzzy inference system"""
    
    def __init__(self, config=None):
        self.logger = logging.getLogger(__name__)
        self.membership = MembershipFunctions()
        self.rule_engine = RuleEngine()
        self.config = config or {}
        
        # Define universe of discourse for each variable
        self.universes = {
            'income': np.linspace(0, 100000, 1000),
            'expenses': np.linspace(0, 80000, 1000),
            'savings': np.linspace(0, 50000, 1000),
            'debt': np.linspace(0, 65000, 1000),
            'risk_tolerance': np.linspace(0, 10, 1000),
            'behavior': np.linspace(0, 100, 1000)
        }
        
        self.logger.info("Fuzzy Inference System initialized")
    
    def fuzzify(self, variable, value):
        """Fuzzify crisp input values"""
        if variable == 'income':
            return self.membership.define_income_memberships(value)
        elif variable == 'expenses':
            return self.membership.define_expense_memberships(value)
        elif variable == 'savings':
            return self.membership.define_savings_memberships(value)
        elif variable == 'debt':
            return self.membership.define_debt_memberships(value)
        elif variable == 'risk_tolerance':
            return self.membership.define_risk_memberships(value)
        else:
            return {}
    
    def evaluate_rules(self, fuzzified_inputs):
        """Evaluate rules against fuzzified inputs"""
        rule_outputs = []
        
        for rule in self.rule_engine.get_rules():
            # Evaluate antecedents
            antecendent_match = True
            min_degree = 1.0
            
            for var, term in rule['if'].items():
                if var in fuzzified_inputs:
                    degree = fuzzified_inputs[var].get(term, 0)
                    min_degree = min(min_degree, degree)
                    if degree == 0:
                        antecendent_match = False
                        break
            
            if antecendent_match and min_degree > 0:
                # Apply rule consequent
                consequent = rule['then']
                consequent['degree'] = min_degree * rule.get('weight', 1.0)
                rule_outputs.append(consequent)
        
        return rule_outputs
    
    def defuzzify(self, rule_outputs, variable='behavior'):
        """Defuzzify using centroid method"""
        if not rule_outputs:
            return 0
        
        # Aggregate outputs
        aggregated = np.zeros_like(self.universes['behavior'])
        
        for output in rule_outputs:
            if variable in output:
                value = output[variable]
                degree = output.get('degree', 0)
                
                # Get membership function for the behavior
                if value == 'cautious':
                    mem_func = self.membership.triangular(
                        self.universes['behavior'], 0, 0, 30
                    )
                elif value == 'moderate':
                    mem_func = self.membership.triangular(
                        self.universes['behavior'], 20, 50, 80
                    )
                elif value == 'aggressive':
                    mem_func = self.membership.triangular(
                        self.universes['behavior'], 60, 85, 100
                    )
                elif value == 'conservative':
                    mem_func = self.membership.triangular(
                        self.universes['behavior'], 0, 15, 40
                    )
                else:
                    mem_func = np.zeros_like(self.universes['behavior'])
                
                # Apply degree
                aggregated = np.maximum(aggregated, np.minimum(mem_func, degree))
        
        # Centroid defuzzification
        if np.sum(aggregated) > 0:
            centroid = np.sum(self.universes['behavior'] * aggregated) / np.sum(aggregated)
            return centroid
        else:
            return 50  # Default moderate behavior
    
    def classify_behavior(self, crisp_inputs):
        """Classify financial behavior from crisp inputs"""
        # Fuzzify inputs
        fuzzified_inputs = {}
        for var, value in crisp_inputs.items():
            if var in ['income', 'expenses', 'savings', 'debt', 'risk_tolerance']:
                fuzzified_inputs[var] = self.fuzzify(var, value)
        
        # Evaluate rules
        rule_outputs = self.evaluate_rules(fuzzified_inputs)
        
        # Defuzzify
        behavior_score = self.defuzzify(rule_outputs, 'behavior')
        
        # Map score to category
        if behavior_score < 25:
            behavior = 'cautious'
        elif behavior_score < 50:
            behavior = 'conservative'
        elif behavior_score < 75:
            behavior = 'moderate'
        else:
            behavior = 'aggressive'
        
        # Get recommended strategies from rules
        strategies = []
        for output in rule_outputs:
            if 'strategy' in output and output['degree'] > 0.3:
                strategies.append(output['strategy'])
        
        # Remove duplicates and limit
        strategies = list(dict.fromkeys(strategies))[:3]
        
        if not strategies:
            strategies = ['budget_planning']  # Default strategy
        
        return {
            'behavior': behavior,
            'score': behavior_score,
            'strategies': strategies,
            'rule_confidence': max([o.get('degree', 0) for o in rule_outputs]) if rule_outputs else 0
        }
    
    def evaluate(self, user_data):
        """Full evaluation of user financial data"""
        crisp_inputs = {
            'income': user_data.get('income', 0),
            'expenses': user_data.get('expenses', 0),
            'savings': user_data.get('savings', 0),
            'debt': user_data.get('debt', 0),
            'risk_tolerance': user_data.get('risk_tolerance', 5)
        }
        
        return self.classify_behavior(crisp_inputs)