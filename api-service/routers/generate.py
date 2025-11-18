"""
Generate Router
Handles package generation requests
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, field_validator
from typing import List
import httpx
import os

router = APIRouter(prefix="/api", tags=["generate"])

GENERATOR_URL = os.getenv('GENERATOR_URL', 'http://localhost:8001')

class MetaQuestionnaireRequest(BaseModel):
    """Request model for meta-questionnaire"""
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

    @field_validator('detail_level')
    @classmethod
    def validate_detail_level(cls, v):
        allowed = ['minimal', 'moderate', 'deep']
        if v not in allowed:
            raise ValueError(f'detail_level must be one of {allowed}')
        return v

    @field_validator('use_case')
    @classmethod
    def validate_use_case(cls, v):
        allowed = ['career', 'learning', 'creative', 'research', 'productivity', 'business']
        if v not in allowed:
            raise ValueError(f'use_case must be one of {allowed}')
        return v

@router.post("/generate")
async def generate_package(request: MetaQuestionnaireRequest):
    """
    Generate customized AI-brain setup package

    Validates request and forwards to Generator Service
    """
    try:
        # Call Generator Service
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GENERATOR_URL}/generate",
                json=request.model_dump()
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Generator service error"
                )

            # Return zip file
            return Response(
                content=response.content,
                media_type="application/zip",
                headers={
                    "Content-Disposition": "attachment; filename=ai-brain-setup.zip"
                }
            )

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Generator service timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Cannot reach generator service: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
