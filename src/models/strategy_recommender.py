"""
Strategy recommender based on fuzzy classification
"""

import logging
from typing import Dict, Any, List

class StrategyRecommender:
    """Recommends financial strategies based on behavior classification"""
    
    def __init__(self, fuzzy_system):
        self.fuzzy_system = fuzzy_system
        self.logger = logging.getLogger(__name__)
        
        # Strategy definitions
        self.strategy_definitions = {
            'budget_planning': {
                'description': 'Create a detailed budget to track and control expenses',
                'priority': 1,
                'actions': [
                    'Track all expenses for 30 days',
                    'Create spending categories',
                    'Set spending limits',
                    'Review weekly budget adherence'
                ]
            },
            'debt_management': {
                'description': 'Develop a plan to reduce and manage debt effectively',
                'priority': 1,
                'actions': [
                    'List all debts with interest rates',
                    'Use avalanche or snowball method',
                    'Negotiate interest rates with creditors',
                    'Consider debt consolidation'
                ]
            },
            'emergency_fund_building': {
                'description': 'Build an emergency fund for financial security',
                'priority': 2,
                'actions': [
                    'Set savings goal of 3-6 months expenses',
                    'Automate monthly savings transfers',
                    'Start with small achievable goals',
                    'Use high-yield savings account'
                ]
            },
            'investment_optimization': {
                'description': 'Optimize investment strategy for growth',
                'priority': 2,
                'actions': [
                    'Diversify investment portfolio',
                    'Review asset allocation',
                    'Consider tax-efficient investments',
                    'Regular portfolio rebalancing'
                ]
            },
            'retirement_planning': {
                'description': 'Plan and prepare for retirement',
                'priority': 2,
                'actions': [
                    'Maximize retirement account contributions',
                    'Utilize employer matching if available',
                    'Create retirement income projections',
                    'Consider catch-up contributions if eligible'
                ]
            },
            'wealth_building': {
                'description': 'Build long-term wealth through strategic planning',
                'priority': 3,
                'actions': [
                    'Increase savings rate to 20%+',
                    'Explore additional income streams',
                    'Invest in growth assets',
                    'Review and optimize tax strategy'
                ]
            },
            'risk_management': {
                'description': 'Manage and mitigate financial risks',
                'priority': 1,
                'actions': [
                    'Review insurance coverage',
                    'Create risk management plan',
                    'Build emergency fund',
                    'Diversify income sources'
                ]
            }
        }
    
    def recommend(self, behavior_result: Dict[str, Any], user_data: Dict[str, Any]) -> List[str]:
        """Recommend strategies based on behavior classification"""
        try:
            strategies = behavior_result.get('strategies', [])
            
            # Add additional strategies based on user data
            additional_strategies = self._get_additional_strategies(user_data)
            
            # Combine and prioritize
            all_strategies = list(dict.fromkeys(strategies + additional_strategies))
            
            # Prioritize strategies
            prioritized = self._prioritize_strategies(all_strategies, user_data)
            
            self.logger.info(f"Recommended {len(prioritized)} strategies for user")
            return prioritized
            
        except Exception as e:
            self.logger.error(f"Strategy recommendation error: {str(e)}")
            return ['budget_planning']
    
    def _get_additional_strategies(self, user_data):
        """Get additional strategies based on user data"""
        strategies = []
        
        income = user_data.get('income', 0)
        savings = user_data.get('savings', 0)
        debt = user_data.get('debt', 0)
        age = user_data.get('age', 30)
        
        # Add strategies based on financial metrics
        if savings < income * 0.1:
            strategies.append('emergency_fund_building')
        
        if debt > income * 0.5:
            strategies.append('debt_management')
        
        if age > 40 and savings < income * 2:
            strategies.append('retirement_planning')
        
        if income > 50000 and savings > income * 0.2:
            strategies.append('investment_optimization')
        
        return strategies
    
    def _prioritize_strategies(self, strategies, user_data):
        """Prioritize strategies based on user needs"""
        prioritized = []
        scores = {}
        
        for strategy in strategies:
            if strategy in self.strategy_definitions:
                score = self.strategy_definitions[strategy]['priority']
                
                # Adjust score based on user data
                if strategy == 'debt_management' and user_data.get('debt', 0) > user_data.get('income', 1) * 0.3:
                    score -= 0.5  # Higher priority
                
                if strategy == 'retirement_planning' and user_data.get('age', 30) > 45:
                    score -= 0.5  # Higher priority
                
                scores[strategy] = score
        
        # Sort by score (lower is higher priority)
        sorted_strategies = sorted(scores.items(), key=lambda x: x[1])
        
        return [s[0] for s in sorted_strategies]
    
    def get_strategy_details(self, strategy_name):
        """Get detailed information about a strategy"""
        return self.strategy_definitions.get(strategy_name, {
            'description': 'Generic financial strategy',
            'actions': ['Review financial situation']
        })