from setuptools import setup, find_packages
import sys

if len(sys.argv) == 1:
    sys.argv.append("install")

setup(
    name="personal_finance_advisor",
    version="1.0.0",
    author="Your Name",
    description="Soft Computing-Based Personal Finance Advisor using Fuzzy Logic",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "scikit-fuzzy>=0.4.2",
        "matplotlib>=3.7.1",
        "seaborn>=0.12.2",
        "pyyaml>=6.0",
        "flask>=2.3.2",
    ],
    python_requires=">=3.8",
)