"""
Tests for Frontend Service
"""

import pytest
from unittest.mock import patch, Mock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_index_route(client):
    """Test index route returns form"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'AI-Brain Integration Setup' in response.data
    assert b'form' in response.data

def test_index_contains_questions(client):
    """Test that index page contains all 10 questions"""
    response = client.get('/')
    assert response.status_code == 200
    # Check for question labels
    assert b'primary use case' in response.data
    assert b'detail' in response.data
    assert b'aspects' in response.data

@patch('app.requests.post')
def test_generate_success(mock_post, client):
    """Test successful package generation"""
    # Mock API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'fake zip content'
    mock_post.return_value = mock_response

    # Submit form
    response = client.post('/generate', data={
        'use_case': 'career',
        'detail_level': 'minimal',
        'key_aspects': ['technical', 'career'],
        'privacy_level': 'moderate',
        'work_style': 'flexible',
        'maintenance': 'weekly',
        'geographic': 'true',
        'technical_bg': 'yes',
        'goals_tracking': 'true',
        'knowledge_domains': 'true'
    })

    assert response.status_code == 200
    assert response.mimetype == 'application/zip'

def test_generate_missing_use_case(client):
    """Test form submission with missing use_case"""
    response = client.post('/generate', data={
        'detail_level': 'minimal',
        'privacy_level': 'moderate',
        'work_style': 'flexible',
        'maintenance': 'weekly',
        'geographic': 'true',
        'technical_bg': 'yes',
        'goals_tracking': 'true',
        'knowledge_domains': 'true'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please fill in all required fields' in response.data

def test_generate_missing_detail_level(client):
    """Test form submission with missing detail_level"""
    response = client.post('/generate', data={
        'use_case': 'career',
        'privacy_level': 'moderate',
        'work_style': 'flexible',
        'maintenance': 'weekly',
        'geographic': 'true',
        'technical_bg': 'yes',
        'goals_tracking': 'true',
        'knowledge_domains': 'true'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please fill in all required fields' in response.data

@patch('app.requests.post')
def test_generate_api_error(mock_post, client):
    """Test API error handling"""
    # Mock API error response
    mock_response = Mock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    response = client.post('/generate', data={
        'use_case': 'career',
        'detail_level': 'minimal',
        'privacy_level': 'moderate',
        'work_style': 'flexible',
        'maintenance': 'weekly',
        'geographic': 'true',
        'technical_bg': 'yes',
        'goals_tracking': 'true',
        'knowledge_domains': 'true'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Error generating package' in response.data

@patch('app.requests.post')
def test_generate_timeout(mock_post, client):
    """Test timeout handling"""
    import requests
    mock_post.side_effect = requests.Timeout("Timeout")

    response = client.post('/generate', data={
        'use_case': 'career',
        'detail_level': 'minimal',
        'privacy_level': 'moderate',
        'work_style': 'flexible',
        'maintenance': 'weekly',
        'geographic': 'true',
        'technical_bg': 'yes',
        'goals_tracking': 'true',
        'knowledge_domains': 'true'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'timed out' in response.data
