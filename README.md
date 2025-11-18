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

**Current Phase:** Local development ready (Sessions 1-5 complete)

**Completed:**
- ✅ Session 1: Repository setup
- ✅ Session 2: Generator Service (12 tests passing)
- ✅ Session 3: API Service (8 tests passing)
- ✅ Session 4: Frontend Service (8 tests passing)
- ✅ Session 5: Docker Compose setup

**Next Steps:**
- Session 6: CI/CD and AWS deployment

## Local Development

### Prerequisites
- Docker
- Docker Compose

### Quick Start

1. Clone repository
2. Navigate to project directory
3. Start all services:
   ```bash
   docker-compose up --build
   ```
4. Open http://localhost:5000
5. Test complete flow

See `LOCAL-TESTING.md` for detailed instructions.

### Testing

```bash
# Run all tests
docker-compose run frontend pytest tests/ -v
docker-compose run api pytest tests/ -v
docker-compose run generator pytest tests/ -v
```

### Individual Service URLs

- **Frontend:** http://localhost:5000
- **API:** http://localhost:8000/docs (Swagger UI)
- **Generator:** http://localhost:8001/docs (Swagger UI)

### Health Checks

```bash
curl http://localhost:5000/health
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## Deployment

*Deployment instructions will be added in Session 6*

## Project Structure

```
ai-brain-setup/
├── frontend-service/          # Flask UI
├── api-service/              # FastAPI orchestration
├── generator-service/        # Package generation
├── docker-compose.yml        # Local development
├── LOCAL-TESTING.md         # Testing guide
└── SESSION-*-SUMMARY.md     # Development logs
```

## License

MIT (or your preferred license)
