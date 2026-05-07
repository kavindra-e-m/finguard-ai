@echo off
echo ========================================
echo FinGuard AI - Complete Setup
echo ========================================
echo.

echo Step 1: Setting up PostgreSQL Database...
echo.
psql -U postgres -c "CREATE DATABASE finguard_db;" 2>nul
psql -U postgres -c "CREATE USER finguard_user WITH PASSWORD 'K@VICLOWn17';" 2>nul
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;" 2>nul
psql -U postgres -d finguard_db -c "GRANT ALL ON SCHEMA public TO finguard_user;" 2>nul
echo [OK] Database setup complete
echo.

echo Step 2: Starting ML Service...
start "FinGuard ML Service" cmd /k "cd ml-service && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo [OK] ML Service starting on port 8000
timeout /t 5 /nobreak > nul
echo.

echo Step 3: Starting Backend...
start "FinGuard Backend" cmd /k "cd backend && mvnw.cmd spring-boot:run"
echo [OK] Backend starting on port 8080
echo Waiting for backend to initialize (30 seconds)...
timeout /t 30 /nobreak
echo.

echo Step 4: Creating Demo User...
curl -X POST http://localhost:8080/api/auth/register -H "Content-Type: application/json" -d "{\"name\":\"Demo User\",\"email\":\"demo@finguard.ai\",\"password\":\"Demo@123\",\"monthlyIncome\":50000}"
echo.
echo [OK] Demo user created
echo.

echo Step 5: Starting Frontend...
start "FinGuard Frontend" cmd /k "cd frontend && npm run dev"
echo [OK] Frontend starting on port 5173
echo.

echo ========================================
echo All Services Started!
echo ========================================
echo.
echo Access the application at: http://localhost:5173
echo.
echo Demo Credentials:
echo   Email: demo@finguard.ai
echo   Password: Demo@123
echo.
echo Services:
echo   - Frontend: http://localhost:5173
echo   - Backend: http://localhost:8080
echo   - ML Service: http://localhost:8000
echo.
pause
