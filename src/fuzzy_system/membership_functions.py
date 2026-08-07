"""
Membership functions for fuzzy logic system
"""

import numpy as np
from typing import Dict, Any

class MembershipFunctions:
    """Defines membership functions for financial variables"""
    
    def __init__(self):
        self.memberships = {}
    
    def _as_array(self, x):
        """Convert scalar or array inputs into a 1D numpy array."""
        return np.atleast_1d(np.asarray(x, dtype=float))
    
    def triangular(self, x, a, b, c):
        """Triangular membership function"""
        values = self._as_array(x)
        result = np.zeros_like(values, dtype=float)

        if not (a <= b <= c):
            raise ValueError('Triangular parameters must satisfy a <= b <= c')

        left_mask = (values > a) & (values < b)
        peak_mask = np.isclose(values, b)
        right_mask = (values > b) & (values < c)

        if b > a:
            result[left_mask] = (values[left_mask] - a) / (b - a)
        if c > b:
            result[right_mask] = (c - values[right_mask]) / (c - b)
        result[peak_mask] = 1.0

        if np.isscalar(x):
            return float(result[0])
        return result
    
    def trapezoidal(self, x, a, b, c, d):
        """Trapezoidal membership function"""
        values = self._as_array(x)
        result = np.zeros_like(values, dtype=float)

        if not (a <= b <= c <= d):
            raise ValueError('Trapezoidal parameters must satisfy a <= b <= c <= d')

        rising_mask = (values > a) & (values < b)
        plateau_mask = (values >= b) & (values <= c)
        falling_mask = (values > c) & (values < d)

        if b > a:
            result[rising_mask] = (values[rising_mask] - a) / (b - a)
        result[plateau_mask] = 1.0
        if d > c:
            result[falling_mask] = (d - values[falling_mask]) / (d - c)

        if np.isscalar(x):
            return float(result[0])
        return result
    
    def gaussian(self, x, mean, sigma):
        """Gaussian membership function"""
        values = self._as_array(x)
        result = np.exp(-0.5 * ((values - mean) / sigma) ** 2)

        if np.isscalar(x):
            return float(result[0])
        return result
    
    def define_income_memberships(self, x):
        """Define income level memberships"""
        return {
            'low': self.triangular(x, 0, 0, 30000),
            'medium': self.triangular(x, 20000, 45000, 70000),
            'high': self.triangular(x, 50000, 80000, 100000)
        }
    
    def define_expense_memberships(self, x):
        """Define expense level memberships"""
        return {
            'low': self.triangular(x, 0, 0, 20000),
            'medium': self.triangular(x, 15000, 35000, 55000),
            'high': self.triangular(x, 40000, 60000, 80000)
        }
    
    def define_savings_memberships(self, x):
        """Define savings level memberships"""
        return {
            'low': self.triangular(x, 0, 0, 10000),
            'medium': self.triangular(x, 5000, 15000, 25000),
            'high': self.triangular(x, 20000, 35000, 50000)
        }
    
    def define_debt_memberships(self, x):
        """Define debt level memberships"""
        return {
            'low': self.triangular(x, 0, 0, 10000),
            'medium': self.triangular(x, 5000, 20000, 35000),
            'high': self.triangular(x, 25000, 45000, 65000)
        }
    
    def define_risk_memberships(self, x):
        """Define risk tolerance memberships"""
        return {
            'low': self.triangular(x, 0, 0, 4),
            'medium': self.triangular(x, 3, 5, 7),
            'high': self.triangular(x, 6, 8, 10)
        }
    
    def define_behavior_memberships(self, x):
        """Define behavior category memberships"""
        return {
            'cautious': self.triangular(x, 0, 0, 30),
            'moderate': self.triangular(x, 20, 50, 80),
            'aggressive': self.triangular(x, 60, 85, 100)
        }