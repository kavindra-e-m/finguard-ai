@echo off
echo ========================================
echo Starting FinGuard Backend
echo ========================================
echo.

cd backend

echo Building backend...
call mvnw.cmd clean install -DskipTests

if %errorlevel% neq 0 (
    echo.
    echo Build failed! Make sure Java 17 is installed.
    pause
    exit /b 1
)

echo.
echo Starting backend server...
start "FinGuard Backend" cmd /k "mvnw.cmd spring-boot:run"

echo.
echo Backend is starting...
echo Wait 30 seconds, then access:
echo - Backend: http://localhost:8080
echo - Swagger: http://localhost:8080/swagger-ui.html
echo - Frontend: http://localhost:5173
echo.
pause
