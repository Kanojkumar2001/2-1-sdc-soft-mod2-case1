#!/usr/bin/env python
"""
Command-line interface for the Personal Finance Advisor
"""

import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.main import FinanceAdvisor

def main():
    """CLI entry point"""
    advisor = FinanceAdvisor()
    
    print("\n" + "="*60)
    print("PERSONAL FINANCE ADVISOR - CLI INTERFACE")
    print("="*60)
    print("\nEnter your financial information:")
    
    try:
        # Collect user input
        user_data = {}
        user_data['user_id'] = input("User ID (optional, press Enter to skip): ") or "user_001"
        user_data['income'] = float(input("Annual Income ($): "))
        user_data['expenses'] = float(input("Annual Expenses ($): "))
        user_data['savings'] = float(input("Total Savings ($): "))
        user_data['debt'] = float(input("Total Debt ($): "))
        user_data['risk_tolerance'] = int(input("Risk Tolerance (1-10): "))
        user_data['age'] = int(input("Age (optional, press Enter to skip): ") or 30)
        
        # Process data
        print("\nProcessing...")
        report = advisor.process_user_data(user_data)
        
        # Display report
        print("\n" + "="*60)
        print("RECOMMENDATION REPORT")
        print("="*60)
        print(f"User ID: {report['user_id']}")
        print(f"Behavior Category: {report['behavior_category']}")
        print(f"Risk Score: {report['risk_score']:.2f}/100")
        print(f"Financial Health Score: {report['financial_health_score']:.2f}/100")
        print("\nRecommended Strategies:")
        for strategy in report['recommended_strategies']:
            print(f"  • {strategy}")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check your input values and try again.")

if __name__ == "__main__":
    main()