"""
API Service - FastAPI application for AI-Brain Setup
Orchestrates business logic and generator service
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="AI-Brain Setup API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GENERATOR_URL = os.getenv('GENERATOR_URL', 'http://localhost:8001')

@app.get("/")
def root():
    """Root endpoint"""
    return {"service": "AI-Brain Setup API", "version": "1.0.0"}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api"}

# Business logic endpoints will be added in Session 3
