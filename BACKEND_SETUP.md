# FinGuard AI - Backend Setup Issue & Solution

## Problem Detected

Your system has **Java 24** installed, but Spring Boot 3.2.0 requires **Java 17 or 21**.
Java 24 is causing compilation errors.

## Solution: Install Correct Java Version

### Step 1: Install Java 17

1. **Download Java 17 (Temurin)**
   - Visit: https://adoptium.net/temurin/releases/?version=17
   - Select: Windows x64 MSI installer
   - Download and install

2. **Set JAVA_HOME Environment Variable**
   ```cmd
   # Open System Properties > Environment Variables
   # Add new System Variable:
   Variable name: JAVA_HOME
   Variable value: C:\Program Files\Eclipse Adoptium\jdk-17.x.x
   
   # Add to PATH:
   %JAVA_HOME%\bin
   ```

3. **Verify Installation**
   ```cmd
   java -version
   # Should show: openjdk version "17.x.x"
   ```

### Step 2: Install PostgreSQL 16

1. **Download PostgreSQL**
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 16 installer
   - Install with default settings
   - Remember the password you set for 'postgres' user

2. **Create Database**
   Open pgAdmin or psql and run:
   ```sql
   CREATE DATABASE finguard_db;
   CREATE USER finguard_user WITH PASSWORD 'finguard_pass';
   GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;
   \c finguard_db
   GRANT ALL ON SCHEMA public TO finguard_user;
   ```

### Step 3: Build Backend

After installing Java 17:

```cmd
cd backend
set "JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.x.x"
set "PATH=%JAVA_HOME%\bin;%PATH%"
mvnw.cmd clean install -DskipTests
```

### Step 4: Run Backend

```cmd
cd backend
mvnw.cmd spring-boot:run
```

Backend will start on: http://localhost:8080

### Step 5: Verify Backend is Running

Open browser or use curl:
```cmd
curl http://localhost:8080/actuator/health
```

Should return: `{"status":"UP"}`

## Frontend is Already Running

Your frontend is already running on http://localhost:5173

Once the backend starts, you can:
1. Go to http://localhost:5173
2. Register with your details:
   - Name: Kavindra
   - Email: kavindra.em2024aiml@sece.ac.in
   - Password: (your password)
   - Monthly Income: 100000

## Quick Reference

| Service | URL | Status |
|---------|-----|--------|
| Frontend | http://localhost:5173 | ✅ Running |
| Backend | http://localhost:8080 | ❌ Needs Java 17 |
| Swagger | http://localhost:8080/swagger-ui.html | After backend starts |

## Current Issue Summary

- ❌ Java 24 is installed (too new)
- ✅ Need Java 17 or 21
- ❌ PostgreSQL may not be installed
- ✅ Frontend is working
- ✅ Maven wrapper is configured

## Next Steps

1. Install Java 17 from the link above
2. Install PostgreSQL 16
3. Create the database
4. Run the backend with the commands above
5. Try registration again on the frontend
