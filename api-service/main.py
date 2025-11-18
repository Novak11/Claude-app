"""
API Service - FastAPI application for AI-Brain Setup
Orchestrates business logic and generator service
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from routers import generate

app = FastAPI(
    title="AI-Brain Setup API",
    version="1.0.0",
    description="API for AI-brain integration package generation"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate.router)

# Configuration
GENERATOR_URL = os.getenv('GENERATOR_URL', 'http://localhost:8001')

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": "AI-Brain Setup API",
        "version": "1.0.0",
        "generator_url": GENERATOR_URL
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api"}
