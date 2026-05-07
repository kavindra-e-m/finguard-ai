# FinGuard AI - Local Development Startup Guide

## Quick Start (Windows)

### Option 1: Automated Startup with PSConsole
Run the provided batch file to start all services in separate windows:
```bash
start-local.bat
```

### Option 2: Manual Startup

#### Step 1: Start PostgreSQL Database
Ensure PostgreSQL is running on localhost:5432

#### Step 2: Start ML Service (Python)
```bash
cd ml-service

# Create/activate virtual environment (first time only)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the service
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
ℹ️  Main startup complete. Loaded 3 models.
```

#### Step 3: Start Backend (Java)
In a new terminal:
```bash
cd backend

# Run with Maven wrapper
mvnw.cmd spring-boot:run
```

**Expected Output:**
```
Started FinGuardApplication in X seconds (JVM running for X.XXX s)
```

#### Step 4: Start Frontend (React)
In a new terminal:
```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
VITE v4.X.X  ready in XXX ms

➜  Local:   http://localhost:5173/
```

## Verification Checklist

### 1. Database Connection
```bash
# Check PostgreSQL is running
netstat -an | findstr :5432

# Or test connection
psql -U finguard_user -d finguard_db -c "SELECT 1;"
```

### 2. Service Health Checks

**ML Service Health:**
```bash
curl http://localhost:8000/health
```

**Backend Health:**
```bash
curl http://localhost:8080/actuator/health
```

**Frontend Accessible:**
```
Open http://localhost:5173 in browser
```

### 3. Documentation

**Backend API Docs (Swagger):**
```
http://localhost:8080/swagger-ui.html
```

**ML Service API Docs:**
```
http://localhost:8000/docs
```

## Database Setup

### First Time Setup

#### 1. Create Database and User
```bash
psql -U postgres

-- Create database
CREATE DATABASE finguard_db;

-- Create user
CREATE USER finguard_user WITH PASSWORD 'finguard_pass';

-- Grant privileges
ALTER ROLE finguard_user WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;

\q
```

#### 2. Verify Connection
```bash
psql -U finguard_user -d finguard_db -c "SELECT 1;"
```

### Database Migrations
Migrations run automatically on Backend startup:
- Spring Boot Hibernate will create/update tables
- Default data migrations if needed

### Seed Sample Data (Optional)

Train ML models and seed demo data:
```bash
# From root directory
cd ml-service

# Install dependencies
pip install -r requirements.txt

# Train ML models
python ml/train_all_models.py

# Seed demo data
python data/seed_data.py
```

## Testing Integration

### 1. User Registration & Login

**Register:**
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Password123!",
    "monthlyIncome": 5000
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "Password123!"
  }'
```

Save the token from response:
```bash
set TOKEN=<token_from_response>
```

### 2. Test Expense Creation

```bash
curl -X POST http://localhost:8080/api/expenses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer %TOKEN%" \
  -d '{
    "category": "FOOD",
    "amount": 45.50,
    "description": "Groceries",
    "expenseDate": "2024-01-15"
  }'
```

### 3. Test ML Integration - Expense Prediction

```bash
curl -X GET http://localhost:8080/api/analytics/predict-expense \
  -H "Authorization: Bearer %TOKEN%"
```

Expected response:
```json
{
  "predictedNextMonth": 1200.50,
  "confidenceLower": 1050.00,
  "confidenceUpper": 1350.00,
  "trend": "upward",
  "forecast3Months": [1200.50, 1250.00, 1300.00]
}
```

### 4. Test Personality Detection

```bash
curl -X GET http://localhost:8080/api/analytics/personality \
  -H "Authorization: Bearer %TOKEN%"
```

### 5. Test Financial Health Score

```bash
curl -X GET http://localhost:8080/api/analytics/financial-health \
  -H "Authorization: Bearer %TOKEN%"
```

### 6. Test Anomaly Detection

```bash
curl -X GET http://localhost:8080/api/analytics/anomalies \
  -H "Authorization: Bearer %TOKEN%"
```

## Troubleshooting

### ML Service Won't Start

**Error:** "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
cd ml-service
pip install -r requirements.txt
```

**Error:** "Port 8000 already in use"

**Solution:**
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or start on different port
python -m uvicorn main:app --reload --port 8001
```

### Backend Won't Start

**Error:** "Database connection refused"

**Solution:**
- Start PostgreSQL
- Update connection string in `backend/src/main/resources/application.properties`
- Check database credentials

**Error:** "Port 8080 already in use"

**Solution:**
```bash
# Kill process on port 8080
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Or change port in application.properties: server.port=8081
```

### Frontend Won't Start

**Error:** "npm: command not found"

**Solution:**
- Install Node.js from https://nodejs.org/ (16+ required)

**Error:** "Port 5173 already in use"

**Solution:**
```bash
# Kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Or let Vite use next available port
npm run dev
```

### Can't Connect to ML Service from Backend

**Error:** "Connection refused"

**Solution:**
- Verify ML service is running: `curl http://localhost:8000/health`
- Check `ML_SERVICE_URL` in `backend/src/main/resources/application.properties` is `http://localhost:8000`
- Check firewall isn't blocking port 8000

### CORS Errors in Frontend

**Error:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution:**
- Update `cors.allowed-origins` in `backend/src/main/resources/application.properties`
- Should include: `http://localhost:5173`

### JWT Token Errors

**Error:** "Unauthorized" or "Invalid token"

**Solution:**
- Clear browser localStorage and re-login
- Check token expiration: `JWT_EXPIRATION=86400000` (24 hours in ms)
- Verify Authorization header format: `Bearer <token>`

## Common Development Tasks

### View Logs

**Backend:**
- Logs appear in console where service runs
- Or check Spring Boot log files if configured

**ML Service:**
```bash
tail -f ml-service/logs/ml_service.log
```

**Frontend:**
- Check browser Developer Tools Console
- Run `npm run dev` verbosely for build logs

### Hot Reload Development

All services support hot reload during development:
- **Frontend:** Auto-reload on `src/` file changes
- **Backend:** Auto-reload on `src/main/java/` changes (with Spring Boot Devtools)
- **ML Service:** Auto-reload on `routes/` and `ml/` changes

### Database Queries

```bash
# Connect to database
psql -U finguard_user -d finguard_db

# View tables
\dt

# View users
SELECT * FROM "user";

# View expenses
SELECT * FROM expense;

# View investments
SELECT * FROM investment;
```

### Git Workflow

Recommended for development:
```bash
# Create feature branch
git checkout -b feature/ml-integration

# Make changes...

# Commit
git add .
git commit -m "feat: implement ML integration"

# Push
git push origin feature/ml-integration

# Create pull request
```

## Performance Tips

1. **Database:**
   - Consider adding indexes on frequently queried columns
   - Use pagination for large result sets

2. **ML Service:**
   - Models are cached in memory on startup
   - Consider model versioning strategy

3. **Frontend:**
   - Use React DevTools to check component performance
   - Monitor network tab in Dev Tools

4. **Backend:**
   - Use Spring Boot Actuator metrics: `http://localhost:8080/actuator/metrics`
   - Enable query logging if needed: `spring.jpa.show-sql=true`

## Next Steps

1. ✅ All services configured for local development
2. ✅ Database setup instructions provided
3. ✅ Integration endpoints documented
4. ✅ Troubleshooting guide included
5. → Start services following "Quick Start" section
6. → Run verification checklist
7. → Test integration with sample API calls
8. → Begin development!

## Support

For issues or questions:
1. Check INTEGRATION_GUIDE.md for detailed architecture
2. Check respective service log files
3. Run health checks to identify failing service
4. Review error messages in browser console
5. Consult backend/ML service documentation
