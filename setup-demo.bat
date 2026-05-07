@echo off
echo ========================================
echo FinGuard AI - Complete Demo Setup
echo ========================================
echo.

echo Step 1: Creating demo user...
echo.
curl -X POST http://localhost:8080/api/auth/register -H "Content-Type: application/json" -d "{\"name\":\"Demo User\",\"email\":\"demo@finguard.ai\",\"password\":\"Demo@123\",\"monthlyIncome\":50000}"
echo.
echo.

echo Step 2: Logging in to get token...
echo.
curl -X POST http://localhost:8080/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"demo@finguard.ai\",\"password\":\"Demo@123\"}" > token.json
echo.
echo.

echo Step 3: Adding sample expenses...
echo Note: You'll need to manually add expenses through the UI or use the token from token.json
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Demo Credentials:
echo   Email: demo@finguard.ai
echo   Password: Demo@123
echo.
echo Access the app at: http://localhost:5173
echo.
pause
