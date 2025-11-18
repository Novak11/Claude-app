"""
Comprehensive tests for Generator Service
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from generator.questionnaire_builder import QuestionnaireBuilder
from generator.package_creator import PackageCreator
from generator.zip_handler import ZipHandler

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "service" in response.json()

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_templates():
    """Test template listing"""
    response = client.get("/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert len(data["templates"]) == 3  # minimal, moderate, deep

def test_generate_package_minimal():
    """Test package generation with minimal template"""
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

    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert len(response.content) > 0  # Has content

def test_generate_package_moderate():
    """Test package generation with moderate template"""
    payload = {
        "use_case": "learning",
        "detail_level": "moderate",
        "key_aspects": ["technical", "career", "communication"],
        "privacy_level": "comprehensive",
        "work_style": "structured",
        "maintenance": "bi-weekly",
        "geographic": False,
        "technical_bg": "somewhat",
        "goals_tracking": True,
        "knowledge_domains": True
    }

    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    assert len(response.content) > 0

def test_generate_package_deep():
    """Test package generation with deep template"""
    payload = {
        "use_case": "comprehensive",
        "detail_level": "deep",
        "key_aspects": ["technical", "career", "communication", "geographic", "work_patterns"],
        "privacy_level": "comprehensive",
        "work_style": "adaptive",
        "maintenance": "monthly",
        "geographic": True,
        "technical_bg": "advanced",
        "goals_tracking": True,
        "knowledge_domains": True
    }

    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    assert len(response.content) > 0

def test_questionnaire_builder():
    """Test QuestionnaireBuilder class"""
    builder = QuestionnaireBuilder()

    # Test template loading
    assert len(builder.templates) == 3
    assert 'minimal' in builder.templates

    # Test template selection
    template = builder.select_template('minimal')
    assert template is not None
    assert 'metadata' in template

    # Test markdown generation
    meta_answers = {
        'detail_level': 'minimal',
        'key_aspects': ['technical', 'career']
    }
    markdown = builder.build(meta_answers)
    assert len(markdown) > 0
    assert "# AI-Brain Integration" in markdown

def test_package_creator():
    """Test PackageCreator class"""
    creator = PackageCreator()

    # Test setup instructions
    meta_answers = {
        'use_case': 'career',
        'maintenance': 'weekly'
    }
    instructions = creator.create_setup_instructions(meta_answers)
    assert len(instructions) > 0
    assert "Setup Instructions" in instructions

    # Test file structure
    structure = creator.create_file_structure()
    assert '1-core/core-identity.md' in structure
    assert '2-active/active-projects.md' in structure

    # Test startup hook
    hook = creator.create_startup_hook()
    assert len(hook) > 0
    assert "#!/bin/bash" in hook

def test_zip_handler():
    """Test ZipHandler class"""
    handler = ZipHandler()

    # Create test package
    zip_bytes = handler.create_package(
        questionnaire_content="# Test Questionnaire",
        setup_instructions="# Test Instructions",
        file_structure={'test.md': 'Test content'},
        startup_hook="#!/bin/bash\necho test"
    )

    assert len(zip_bytes) > 0
    # Verify it's a valid zip
    import zipfile
    import io
    with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zf:
        assert 'questionnaire.md' in zf.namelist()
        assert 'README.md' in zf.namelist()

def test_template_selection_logic():
    """Test template selection with various inputs"""
    builder = QuestionnaireBuilder()

    # Test valid selections
    assert builder.select_template('minimal') == builder.templates['minimal']
    assert builder.select_template('moderate') == builder.templates['moderate']
    assert builder.select_template('deep') == builder.templates['deep']

    # Test default to moderate for invalid input
    assert builder.select_template('invalid') == builder.templates['moderate']
    assert builder.select_template('') == builder.templates['moderate']

def test_question_filtering():
    """Test question filtering logic"""
    builder = QuestionnaireBuilder()

    template = builder.select_template('moderate')
    meta_answers = {
        'detail_level': 'moderate',
        'key_aspects': ['technical', 'career']
    }

    filtered = builder.filter_questions(template, meta_answers)

    # High priority categories should be included
    assert 'cognitive_profile' in filtered['categories']
    assert 'career_context' in filtered['categories']

    # Technical aspect should include technical_background
    assert 'technical_background' in filtered['categories']

def test_markdown_generation_formats():
    """Test markdown generation for different question types"""
    builder = QuestionnaireBuilder()

    meta_answers = {
        'detail_level': 'minimal',
        'key_aspects': ['technical', 'career', 'communication']
    }

    markdown = builder.build(meta_answers)

    # Should contain multiple choice checkboxes
    assert "- [ ]" in markdown

    # Should contain short text placeholders
    assert "**Your answer:**" in markdown

    # Should contain section headers
    assert "##" in markdown
