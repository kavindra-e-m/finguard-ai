@echo off
echo ========================================
echo FinGuard AI - Starting All Services
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo [1/5] Starting PostgreSQL Database...
docker-compose up -d postgres
timeout /t 10 /nobreak >nul

echo [2/5] Starting ML Service...
docker-compose up -d ml-service
timeout /t 15 /nobreak >nul

echo [3/5] Starting Backend Service...
docker-compose up -d backend
timeout /t 20 /nobreak >nul

echo [4/5] Starting Frontend Service...
docker-compose up -d frontend
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo All Services Started Successfully!
echo ========================================
echo.
echo Services:
echo - Frontend:  http://localhost:5173
echo - Backend:   http://localhost:8080
echo - ML API:    http://localhost:8000
echo - Swagger:   http://localhost:8080/swagger-ui.html
echo.
echo Demo Credentials:
echo Email: demo@finguard.ai
echo Password: Demo@123
echo.
echo To view logs: docker-compose logs -f
echo To stop all:  docker-compose down
echo.
pause
