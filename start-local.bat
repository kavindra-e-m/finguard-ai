@echo off
echo ========================================
echo FinGuard AI - Local Development Setup
echo ========================================
echo.

REM Check PostgreSQL
echo Checking PostgreSQL connection...
psql -U finguard_user -d finguard_db -c "SELECT 1;" >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: PostgreSQL not accessible. Make sure it's running on localhost:5432
    echo Database: finguard_db, User: finguard_user, Password: finguard_pass
    echo.
)

echo Starting services in separate windows...
echo.

REM Start ML Service
echo [1/3] Starting ML Service on port 8000...
start "FinGuard ML Service" cmd /k "cd ml-service && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul

REM Start Backend
echo [2/3] Starting Backend on port 8080...
start "FinGuard Backend" cmd /k "cd backend && mvnw.cmd spring-boot:run"
timeout /t 5 /nobreak >nul

REM Start Frontend
echo [3/3] Starting Frontend on port 5173...
start "FinGuard Frontend" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ========================================
echo All Services Starting...
echo ========================================
echo.
echo Wait for all services to start, then access:
echo - Frontend:  http://localhost:5173
echo - Backend:   http://localhost:8080
echo - ML API:    http://localhost:8000
echo.
pause
