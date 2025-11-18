"""
Frontend Service - Flask application for AI-Brain Setup
Handles user interface and meta-questionnaire
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import requests
import os
import io

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
API_URL = os.getenv('API_URL', 'http://localhost:8000')
PORT = int(os.getenv('PORT', 5000))

@app.route('/')
def index():
    """Display meta-questionnaire"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Process form and generate package"""
    try:
        # Collect form data
        form_data = {
            'use_case': request.form.get('use_case'),
            'detail_level': request.form.get('detail_level'),
            'key_aspects': request.form.getlist('key_aspects'),
            'privacy_level': request.form.get('privacy_level'),
            'work_style': request.form.get('work_style'),
            'maintenance': request.form.get('maintenance'),
            'geographic': request.form.get('geographic') == 'true',
            'technical_bg': request.form.get('technical_bg'),
            'goals_tracking': request.form.get('goals_tracking') == 'true',
            'knowledge_domains': request.form.get('knowledge_domains') == 'true',
        }

        # Validate required fields
        if not form_data['use_case'] or not form_data['detail_level']:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('index'))

        # Call API Service
        response = requests.post(
            f"{API_URL}/api/generate",
            json=form_data,
            timeout=60
        )

        if response.status_code == 200:
            # Return zip file
            return send_file(
                io.BytesIO(response.content),
                mimetype='application/zip',
                as_attachment=True,
                download_name='ai-brain-setup.zip'
            )
        else:
            flash(f'Error generating package: {response.status_code}', 'error')
            return redirect(url_for('index'))

    except requests.Timeout:
        flash('Request timed out. Please try again.', 'error')
        return redirect(url_for('index'))
    except requests.RequestException as e:
        flash(f'Cannot reach API service: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Unexpected error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "frontend"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
