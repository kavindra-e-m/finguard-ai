@echo off
cls
echo ========================================
echo FinGuard AI - Quick Fix
echo ========================================
echo.

echo Step 1: Testing Backend Connection...
curl -s http://localhost:8080/actuator/health
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Backend is NOT responding!
    echo.
    echo Please check:
    echo 1. Is the backend terminal running?
    echo 2. Are there any errors in the backend terminal?
    echo 3. Is PostgreSQL database running?
    echo.
    pause
    exit /b 1
)
echo.
echo [OK] Backend is responding
echo.

echo Step 2: Creating Demo User...
echo.
curl -v -X POST http://localhost:8080/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Demo User\",\"email\":\"demo@finguard.ai\",\"password\":\"Demo@123\",\"monthlyIncome\":50000}"
echo.
echo.

echo Step 3: Testing Login...
echo.
curl -v -X POST http://localhost:8080/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"demo@finguard.ai\",\"password\":\"Demo@123\"}"
echo.
echo.

echo ========================================
echo.
echo If you see a token above, login should work!
echo Try logging in at: http://localhost:5173
echo.
echo Credentials:
echo   Email: demo@finguard.ai
echo   Password: Demo@123
echo.
pause
