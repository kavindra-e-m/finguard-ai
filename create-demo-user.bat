@echo off
echo ========================================
echo Creating Demo User via API
echo ========================================
echo.
echo Waiting for backend to be ready...
timeout /t 5 /nobreak > nul

curl -X POST http://localhost:8080/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Demo User\",\"email\":\"demo@finguard.ai\",\"password\":\"Demo@123\",\"monthlyIncome\":50000}"

echo.
echo.
echo ========================================
echo Demo user created!
echo Email: demo@finguard.ai
echo Password: Demo@123
echo ========================================
pause
