# FinGuard AI - Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Docker Desktop installed and running
- ✅ Java 17+ (for local development)
- ✅ Node.js 20+ (for local development)
- ✅ Python 3.11+ (for local development)
- ✅ PostgreSQL 16 (for local development)

## Option 1: Docker Compose (Recommended)

### Step 1: Start All Services
```bash
# Windows
start.bat

# Or manually
docker-compose up --build
```

### Step 2: Wait for Services to Start
- PostgreSQL: ~10 seconds
- ML Service: ~15 seconds
- Backend: ~30 seconds
- Frontend: ~10 seconds

### Step 3: Train ML Models
```bash
docker exec finguard-ml-service python ml/train_all_models.py
```

### Step 4: Seed Demo Data (Optional)
```bash
docker exec finguard-ml-service python data/seed_data.py
```

### Step 5: Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080
- Swagger Docs: http://localhost:8080/swagger-ui.html
- ML Service: http://localhost:8000/docs

## Option 2: Local Development

### Step 1: Setup PostgreSQL
```bash
# Create database and user
psql -U postgres
CREATE DATABASE finguard_db;
CREATE USER finguard_user WITH PASSWORD 'finguard_pass';
GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;
```

### Step 2: Start Services
```bash
# Windows - Opens 3 terminal windows
start-local.bat

# Or manually start each service:

# Terminal 1 - ML Service
cd ml-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 - Backend
cd backend
mvnw.cmd spring-boot:run

# Terminal 3 - Frontend
cd frontend
npm install
npm run dev
```

## Verify Connectivity

### Test Backend Health
```bash
curl http://localhost:8080/actuator/health
```

### Test ML Service Health
```bash
curl http://localhost:8000/health
```

### Test Frontend
Open browser: http://localhost:5173

## Demo Credentials
```
Email: demo@finguard.ai
Password: Demo@123
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
netstat -ano | findstr :8080
netstat -ano | findstr :5173
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### Database Connection Failed
- Ensure PostgreSQL is running
- Check credentials in .env files
- Verify database exists: `psql -U finguard_user -d finguard_db`

### CORS Errors
- Ensure backend CORS_ALLOWED_ORIGINS includes http://localhost:5173
- Check browser console for specific errors
- Verify frontend VITE_API_URL is http://localhost:8080

### Docker Issues
```bash
# Stop all containers
docker-compose down

# Remove volumes and restart
docker-compose down -v
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ml-service
```

## Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React UI |
| Backend | http://localhost:8080 | Spring Boot API |
| Swagger | http://localhost:8080/swagger-ui.html | API Docs |
| ML Service | http://localhost:8000 | FastAPI ML |
| ML Docs | http://localhost:8000/docs | ML API Docs |
| PostgreSQL | localhost:5432 | Database |

## Next Steps

1. Register a new user or use demo credentials
2. Add expenses manually or import CSV
3. View financial health dashboard
4. Check predictions and analytics
5. Optimize investment portfolio

## Stopping Services

### Docker
```bash
docker-compose down
```

### Local Development
Close the terminal windows or press Ctrl+C in each terminal
