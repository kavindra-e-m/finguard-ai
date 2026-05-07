@echo off
echo ========================================
echo FinGuard AI - Service Diagnostics
echo ========================================
echo.

echo [1/5] Checking if Backend is running...
curl -s http://localhost:8080/actuator/health 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Backend is NOT running on port 8080
    echo Please start the backend first: run-backend.bat
    echo.
    pause
    exit /b 1
)
echo [OK] Backend is running
echo.

echo [2/5] Checking if ML Service is running...
curl -s http://localhost:8000/health 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] ML Service is NOT running on port 8000
    echo Start it with: run-ml-service.bat
) else (
    echo [OK] ML Service is running
)
echo.

echo [3/5] Checking if Frontend is running...
curl -s http://localhost:5173 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Frontend is NOT running on port 5173
    echo Start it with: run-frontend.bat
) else (
    echo [OK] Frontend is running
)
echo.

echo [4/5] Testing Backend Registration Endpoint...
echo Attempting to register test user...
curl -X POST http://localhost:8080/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test%RANDOM%@test.com\",\"password\":\"Test@123\",\"monthlyIncome\":50000}" ^
  -w "\nHTTP Status: %%{http_code}\n"
echo.

echo [5/5] Registering Demo User...
curl -X POST http://localhost:8080/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Demo User\",\"email\":\"demo@finguard.ai\",\"password\":\"Demo@123\",\"monthlyIncome\":50000}" ^
  -w "\nHTTP Status: %%{http_code}\n"
echo.

echo ========================================
echo Diagnostic Complete
echo ========================================
echo.
echo If registration succeeded, you can now login with:
echo   Email: demo@finguard.ai
echo   Password: Demo@123
echo.
echo Access the app at: http://localhost:5173
echo.
pause
