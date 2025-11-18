"""
Frontend Service - Flask application for AI-Brain Setup
Handles user interface and meta-questionnaire
"""

from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# Configuration
API_URL = os.getenv('API_URL', 'http://localhost:8000')
PORT = int(os.getenv('PORT', 5000))

@app.route('/')
def index():
    """Display meta-questionnaire"""
    # Implementation in Session 4
    return "Frontend Service - Coming in Session 4"

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "frontend"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
