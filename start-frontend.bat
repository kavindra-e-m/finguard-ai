@echo off
echo ========================================
echo FinGuard AI - Starting Frontend
echo ========================================
echo.

echo Starting Frontend Development Server...
cd frontend
start "FinGuard Frontend" cmd /k "npm run dev"

echo.
echo Frontend starting on http://localhost:5173
echo.
echo NOTE: You need to start the backend separately:
echo 1. Install Java 17+
echo 2. Run: cd backend ^&^& mvnw.cmd spring-boot:run
echo.
echo And ML Service:
echo 1. Install Python 3.11+
echo 2. Run: cd ml-service ^&^& python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt ^&^& uvicorn main:app --reload
echo.
pause
