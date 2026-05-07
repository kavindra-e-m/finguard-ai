# FinGuard AI - Integration - QUICK REFERENCE

## 🚀 Quick Start (Choose One)

### Option A: Docker (Easiest)
```bash
docker-compose up --build
# Then access: http://localhost:5173
```

### Option B: Local Development
```bash
# Terminal 1: ML Service
cd ml-service && python -m uvicorn main:app --reload --port 8000

# Terminal 2: Backend
cd backend && mvnw.cmd spring-boot:run

# Terminal 3: Frontend
cd frontend && npm run dev
```

### Option C: Auto Script
```bash
start-local.bat
```

## 🔍 Verify Integration

```bash
.\verify-integration.ps1
```

Or manually:
```bash
curl http://localhost:5173              # Frontend
curl http://localhost:8080/actuator/health  # Backend
curl http://localhost:8000/health        # ML Service
```

## 📍 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8080 |
| Backend Docs | http://localhost:8080/swagger-ui.html |
| ML Service | http://localhost:8000 |
| ML Service Docs | http://localhost:8000/docs |
| Database | localhost:5432 |

## 📚 Documentation Files

1. **INTEGRATION_COMPLETE.md** - Overview (start here)
2. **LOCAL_DEVELOPMENT.md** - Step-by-step setup guide
3. **INTEGRATION_GUIDE.md** - Detailed architecture
4. **API_REFERENCE.md** - All endpoints with examples
5. **README.md** - Updated with integration info

## 🔐 Test User

```
Email: demo@finguard.ai
Password: Demo@123
```

## 🧪 Test API Call

```bash
# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@finguard.ai","password":"Demo@123"}'

# Copy the token from response

# Predict expenses
curl http://localhost:8080/api/analytics/predict-expense \
  -H "Authorization: Bearer <TOKEN>"
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in config or kill process |
| ML Service 404 | Check routes registered in main.py |
| Backend can't reach ML Service | Verify ML_SERVICE_URL in application.properties |
| CORS errors | Update cors.allowed-origins in application.properties |
| Database connection fails | Ensure PostgreSQL running, check credentials |
| JWT token invalid | Clear localStorage and re-login |

## 📊 Integration Flow

```
User (Frontend)
    ↓ Login/Register
    ↓ Add Expenses
    ↓ View Analytics
Backend (Spring Boot)
    ↓ Authenticate (JWT)
    ↓ Extract Features
    ↓ Call ML Service
ML Service (FastAPI)
    ↓ Load Models
    ↓ Process Features
    ↓ Return Predictions
Backend (Format Response)
    ↓ Return to Frontend
Frontend (Display Results)
```

## 🛠️ Environment Configuration

**Root `.env`:**
```env
ML_SERVICE_URL=http://localhost:8000
BACKEND_URL=http://localhost:8080
POSTGRES_DB=finguard_db
POSTGRES_USER=finguard_user
POSTGRES_PASSWORD=finguard_pass
```

**Frontend `.env`:**
```env
VITE_API_URL=http://localhost:8080
VITE_ML_SERVICE_URL=http://localhost:8000
```

**ML Service `.env`:**
```env
DATABASE_URL=postgresql://finguard_user:finguard_pass@localhost:5432/finguard_db
MODEL_PATH=./models
LOG_LEVEL=INFO
```

## 📋 Integration Checklist

- [ ] Started PostgreSQL on port 5432
- [ ] Started ML Service on port 8000
- [ ] Started Backend on port 8080
- [ ] Started Frontend on port 5173
- [ ] Ran verify-integration.ps1 - all green
- [ ] Can access Frontend at http://localhost:5173
- [ ] Can login/register
- [ ] Can add expense
- [ ] Can view analytics predictions
- [ ] All API endpoints working

## 🎯 ML Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/analytics/predict-expense | GET | Forecast expenses |
| /api/analytics/personality | GET | Financial personality |
| /api/analytics/stress | GET | Financial stress level |
| /api/analytics/financial-health | GET | Health score |
| /api/analytics/anomalies | GET | Detect anomalies |

All endpoints require JWT authentication via `Authorization: Bearer <token>` header.

## 💾 Database

Connection string for tools:
```
postgresql://finguard_user:finguard_pass@localhost:5432/finguard_db
```

Quick test:
```bash
psql -U finguard_user -d finguard_db -c "SELECT 1;"
```

## 📞 Need Help?

1. Check documentation files (listed above)
2. Run `verify-integration.ps1`
3. Check service logs
4. Review troubleshooting section in LOCAL_DEVELOPMENT.md

## ✅ Status

**Integration Status**: ✅ COMPLETE

All services configured and documented.
Ready for local development and testing.
