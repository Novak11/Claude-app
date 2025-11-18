"""
Generator Service - Package generation for AI-Brain Setup
Creates customized questionnaires and setup packages
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os

from generator.questionnaire_builder import QuestionnaireBuilder
from generator.package_creator import PackageCreator
from generator.zip_handler import ZipHandler

app = FastAPI(title="Generator Service", version="1.0.0")

PORT = int(os.getenv('PORT', 8001))

# Initialize components
questionnaire_builder = QuestionnaireBuilder()
package_creator = PackageCreator()
zip_handler = ZipHandler()

# Request models
class MetaAnswers(BaseModel):
    """Meta-questionnaire answers"""
    use_case: str
    detail_level: str
    key_aspects: List[str]
    privacy_level: str
    work_style: str
    maintenance: str
    geographic: bool
    technical_bg: str
    goals_tracking: bool
    knowledge_domains: bool

@app.get("/")
def root():
    """Root endpoint"""
    return {"service": "Generator Service", "version": "1.0.0"}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "generator"}

@app.post("/generate")
async def generate_package(meta_answers: MetaAnswers):
    """
    Generate customized AI-brain setup package

    Args:
        meta_answers: User's meta-questionnaire responses

    Returns:
        Zip file with customized package
    """
    try:
        # Convert to dict
        answers_dict = meta_answers.model_dump()

        # Build questionnaire
        questionnaire_content = questionnaire_builder.build(answers_dict)

        # Create setup instructions
        setup_instructions = package_creator.create_setup_instructions(answers_dict)

        # Create file structure
        file_structure = package_creator.create_file_structure()

        # Create startup hook
        startup_hook = package_creator.create_startup_hook()

        # Create zip package
        zip_bytes = zip_handler.create_package(
            questionnaire_content,
            setup_instructions,
            file_structure,
            startup_hook
        )

        # Return as downloadable file
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=ai-brain-setup.zip"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates")
def list_templates():
    """List available question templates"""
    return {
        "templates": list(questionnaire_builder.templates.keys()),
        "count": len(questionnaire_builder.templates)
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=PORT)
