@echo off
echo ========================================
echo Testing FinGuard AI Services
echo ========================================
echo.

echo Testing Frontend (Port 5173)...
curl -s http://localhost:5173 > nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Frontend is running
) else (
    echo [FAIL] Frontend is NOT running
)
echo.

echo Testing Backend (Port 8080)...
curl -s http://localhost:8080/actuator/health
if %errorlevel% equ 0 (
    echo [OK] Backend is running
) else (
    echo [FAIL] Backend is NOT running
)
echo.

echo Testing ML Service (Port 8000)...
curl -s http://localhost:8000/health
if %errorlevel% equ 0 (
    echo [OK] ML Service is running
) else (
    echo [FAIL] ML Service is NOT running
)
echo.

echo ========================================
echo Testing Registration Endpoint...
echo ========================================
curl -v -X POST http://localhost:8080/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test@test.com\",\"password\":\"Test@123\",\"monthlyIncome\":50000}"
echo.
echo.

pause
