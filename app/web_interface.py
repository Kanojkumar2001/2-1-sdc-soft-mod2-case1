"""
Web interface for the Personal Finance Advisor
"""

from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.main import FinanceAdvisor

app = Flask(__name__, template_folder=str(Path(__file__).parent / 'templates'))
advisor = FinanceAdvisor()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze user financial data"""
    try:
        user_data = request.get_json()
        
        # Process data
        report = advisor.process_user_data(user_data)
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)