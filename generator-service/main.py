"""
Generator Service - Package generation for AI-Brain Setup
Creates customized questionnaires and setup packages
"""

from fastapi import FastAPI
import os

app = FastAPI(title="Generator Service", version="1.0.0")

PORT = int(os.getenv('PORT', 8001))

@app.get("/")
def root():
    """Root endpoint"""
    return {"service": "Generator Service", "version": "1.0.0"}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "generator"}

# Package generation logic will be added in Session 2

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=PORT)
