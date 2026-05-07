@echo off
echo ========================================
echo FinGuard AI - Backend Setup
echo ========================================
echo.

echo Checking Java installation...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Java is not installed or not in PATH
    echo Please install Java 17+ from: https://adoptium.net/temurin/releases/?version=17
    echo.
    pause
    exit /b 1
)

echo Java found!
echo.

echo Installing Maven Wrapper...
cd backend
if not exist ".mvn" mkdir .mvn

echo Downloading Maven Wrapper...
powershell -Command "& {Invoke-WebRequest -Uri 'https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.2.0/maven-wrapper-3.2.0.jar' -OutFile '.mvn/wrapper/maven-wrapper.jar'}"

echo Creating mvnw.cmd...
powershell -Command "& {Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/takari/maven-wrapper/master/mvnw.cmd' -OutFile 'mvnw.cmd'}"

echo Creating mvnw...
powershell -Command "& {Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/takari/maven-wrapper/master/mvnw' -OutFile 'mvnw'}"

echo.
echo Maven Wrapper installed successfully!
echo.
echo Starting backend server...
call mvnw.cmd spring-boot:run

pause
