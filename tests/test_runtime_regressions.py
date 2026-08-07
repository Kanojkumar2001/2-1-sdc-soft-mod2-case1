import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.main import FinanceAdvisor
from src.utils.validators import InputValidator


class TestRuntimeRegressions(unittest.TestCase):
    def test_finance_advisor_resolves_config_from_any_cwd(self):
        original_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                advisor = FinanceAdvisor()
                sample_user = {
                    'user_id': 7,
                    'age': 30,
                    'income': 50000,
                    'expenses': 30000,
                    'savings': 15000,
                    'debt': 8000,
                    'risk_tolerance': 6,
                    'investment_knowledge': 5,
                    'financial_goals': 'wealth_building',
                    'employment_status': 'employed',
                    'dependents': 1
                }
                report = advisor.process_user_data(sample_user)
                self.assertIn('behavior_category', report)
                self.assertIn('recommended_strategies', report)
            finally:
                os.chdir(original_cwd)

    def test_validator_rejects_non_mapping_input(self):
        validator = InputValidator()
        is_valid, errors = validator.validate_user_data(None)
        self.assertFalse(is_valid)
        self.assertTrue(any('must be a dictionary' in error for error in errors))


if __name__ == '__main__':
    unittest.main()