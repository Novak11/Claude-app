# Local Development & Testing Guide

## Prerequisites

- Docker installed
- Docker Compose installed

## Quick Start

### 1. Build and Start All Services

```bash
docker-compose up --build
```

This will:
- Build all 3 Docker images
- Start all 3 services
- Connect them via internal network

### 2. Access the Application

Open browser: http://localhost:5000

### 3. Test Complete Flow

1. Fill out meta-questionnaire (10 questions)
2. Click "Generate My Setup Package"
3. Download should start (ai-brain-setup.zip)
4. Unzip and verify contents

### 4. Stop Services

```bash
docker-compose down
```

---

## Individual Service URLs

- **Frontend:** http://localhost:5000
- **API:** http://localhost:8000
- **Generator:** http://localhost:8001

### Health Checks

```bash
curl http://localhost:5000/health
curl http://localhost:8000/health
curl http://localhost:8001/health
```

---

## Testing Individual Services

### Test Generator Service Directly

```bash
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "use_case": "career",
    "detail_level": "minimal",
    "key_aspects": ["technical", "career"],
    "privacy_level": "moderate",
    "work_style": "flexible",
    "maintenance": "weekly",
    "geographic": true,
    "technical_bg": "yes",
    "goals_tracking": true,
    "knowledge_domains": true
  }' \
  --output test-package.zip
```

### Test API Service

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "use_case": "learning",
    "detail_level": "moderate",
    "key_aspects": ["technical"],
    "privacy_level": "moderate",
    "work_style": "flexible",
    "maintenance": "weekly",
    "geographic": false,
    "technical_bg": "yes",
    "goals_tracking": true,
    "knowledge_domains": false
  }' \
  --output test-package-api.zip
```

---

## Running Tests

### Run All Service Tests

```bash
# Frontend tests
docker-compose run frontend pytest tests/ -v

# API tests
docker-compose run api pytest tests/ -v

# Generator tests
docker-compose run generator pytest tests/ -v
```

---

## Troubleshooting

### Services Won't Start

Check logs:
```bash
docker-compose logs frontend
docker-compose logs api
docker-compose logs generator
```

### Port Already in Use

Change ports in docker-compose.yml:
```yaml
ports:
  - "5001:5000"  # Change 5001 to any available port
```

### Cannot Connect Between Services

Verify network:
```bash
docker network ls
docker network inspect claude-app_app-network
```

---

## Development Workflow

### Make Code Changes

1. Edit code in service folder
2. Rebuild specific service:
   ```bash
   docker-compose up --build frontend
   ```
3. Test changes

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
```

### Restart Service

```bash
docker-compose restart frontend
```

---

## Next Steps

After local testing is successful:
- Session 6 (CLI): AWS deployment & CI/CD
