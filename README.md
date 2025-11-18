# AI-Brain Setup Application

A microservices web application that helps users create their own AI persistent memory system.

## Overview

This application guides users through creating a customized AI-brain integration:
1. User completes a meta-questionnaire (10 questions)
2. App generates a personalized setup package
3. Package includes customized questions, instructions, and file templates
4. User downloads and implements locally

## Architecture

- **Frontend Service** (Flask, port 5000): User interface
- **API Service** (FastAPI, port 8000): Business logic orchestration
- **Generator Service** (Python, port 8001): Package generation

## Tech Stack

- Python 3.11+
- Flask (Frontend)
- FastAPI (API)
- Docker & Docker Compose
- pytest (Testing)
- GitHub Actions (CI/CD)
- AWS ECS Fargate (Deployment)

## Development Status

**Current Phase:** Repository setup complete

**Next Steps:**
- Session 2: Implement Generator Service
- Session 3: Implement API Service
- Session 4: Implement Frontend Service
- Session 5: Local development with docker-compose
- Session 6: CI/CD and AWS deployment

## Local Development

*Instructions will be added in Session 5*

## Testing

*Testing instructions will be added as services are implemented*

## Deployment

*Deployment instructions will be added in Session 6*

## Project Structure

See file tree above for complete structure.

## License

MIT (or your preferred license)
