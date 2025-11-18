"""
Comprehensive tests for API Service
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()
    assert "generator_url" in response.json()

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_endpoint_validation():
    """Test request validation"""
    # Invalid detail_level
    payload = {
        "use_case": "career",
        "detail_level": "invalid",  # Invalid
        "key_aspects": ["technical"],
        "privacy_level": "moderate",
        "work_style": "flexible",
        "maintenance": "weekly",
        "geographic": True,
        "technical_bg": "yes",
        "goals_tracking": True,
        "knowledge_domains": True
    }

    response = client.post("/api/generate", json=payload)
    assert response.status_code == 422  # Validation error

def test_generate_endpoint_invalid_use_case():
    """Test invalid use_case validation"""
    payload = {
        "use_case": "invalid_case",  # Invalid
        "detail_level": "minimal",
        "key_aspects": ["technical"],
        "privacy_level": "moderate",
        "work_style": "flexible",
        "maintenance": "weekly",
        "geographic": True,
        "technical_bg": "yes",
        "goals_tracking": True,
        "knowledge_domains": True
    }

    response = client.post("/api/generate", json=payload)
    assert response.status_code == 422  # Validation error

def test_generate_endpoint_missing_field():
    """Test missing required field"""
    payload = {
        "use_case": "career",
        "detail_level": "minimal",
        # Missing other required fields
    }

    response = client.post("/api/generate", json=payload)
    assert response.status_code == 422

@patch('routers.generate.httpx.AsyncClient')
def test_generate_endpoint_success(mock_client):
    """Test successful package generation"""
    # Mock Generator Service response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'fake zip content'

    # Create async context manager mock
    mock_context = AsyncMock()
    mock_context.post = AsyncMock(return_value=mock_response)
    mock_client.return_value.__aenter__.return_value = mock_context

    payload = {
        "use_case": "career",
        "detail_level": "minimal",
        "key_aspects": ["technical", "career"],
        "privacy_level": "moderate",
        "work_style": "flexible",
        "maintenance": "weekly",
        "geographic": True,
        "technical_bg": "yes",
        "goals_tracking": True,
        "knowledge_domains": True
    }

    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"

@patch('routers.generate.httpx.AsyncClient')
def test_generate_endpoint_generator_error(mock_client):
    """Test Generator Service error handling"""
    # Mock Generator Service error
    mock_response = Mock()
    mock_response.status_code = 500

    # Create async context manager mock
    mock_context = AsyncMock()
    mock_context.post = AsyncMock(return_value=mock_response)
    mock_client.return_value.__aenter__.return_value = mock_context

    payload = {
        "use_case": "career",
        "detail_level": "minimal",
        "key_aspects": ["technical"],
        "privacy_level": "moderate",
        "work_style": "flexible",
        "maintenance": "weekly",
        "geographic": True,
        "technical_bg": "yes",
        "goals_tracking": True,
        "knowledge_domains": True
    }

    response = client.post("/api/generate", json=payload)
    assert response.status_code == 500

@patch('routers.generate.httpx.AsyncClient')
def test_generate_endpoint_timeout(mock_client):
    """Test timeout handling"""
    import httpx

    # Create async context manager mock that raises timeout
    mock_context = AsyncMock()
    mock_context.post = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))
    mock_client.return_value.__aenter__.return_value = mock_context

    payload = {
        "use_case": "career",
        "detail_level": "minimal",
        "key_aspects": ["technical"],
        "privacy_level": "moderate",
        "work_style": "flexible",
        "maintenance": "weekly",
        "geographic": True,
        "technical_bg": "yes",
        "goals_tracking": True,
        "knowledge_domains": True
    }

    response = client.post("/api/generate", json=payload)
    assert response.status_code == 504  # Gateway Timeout
