# FinGuard AI - Complete Setup Guide

## Issue: Registration Failed

The registration is failing because the **backend server is not running**. The frontend is trying to connect to `http://localhost:8080` but nothing is listening there.

## Solution: Start the Backend Server

### Prerequisites Needed

1. **Java 17+** - Download from: https://adoptium.net/temurin/releases/?version=17
2. **PostgreSQL 16** - Download from: https://www.postgresql.org/download/windows/
3. **Python 3.11+** - Download from: https://www.python.org/downloads/

### Step-by-Step Setup

#### 1. Install Java 17

```bash
# Download and install Java 17 from:
https://adoptium.net/temurin/releases/?version=17

# After installation, verify:
java -version
# Should show: openjdk version "17.x.x"
```

#### 2. Install PostgreSQL

```bash
# Download and install PostgreSQL 16 from:
https://www.postgresql.org/download/windows/

# During installation:
- Set password for postgres user (remember this!)
- Keep default port: 5432
- Install pgAdmin (recommended)
```

#### 3. Create Database

Open **pgAdmin** or **psql** and run:

```sql
CREATE DATABASE finguard_db;
CREATE USER finguard_user WITH PASSWORD 'finguard_pass';
GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;
\c finguard_db
GRANT ALL ON SCHEMA public TO finguard_user;
```

Or use psql command line:

```bash
psql -U postgres
# Enter your postgres password
# Then run the SQL commands above
```

#### 4. Setup Backend

```bash
# Option A: Use setup script
setup-backend.bat

# Option B: Manual setup
cd backend

# Download Maven if needed, then:
mvn clean install
mvn spring-boot:run
```

#### 5. Verify Backend is Running

Open browser or use curl:

```bash
# Check health endpoint
curl http://localhost:8080/actuator/health

# Should return: {"status":"UP"}
```

#### 6. Now Try Registration Again

Go to: http://localhost:5173/register

Fill in:
- Name: Kavindra
- Email: kavindra.em2024aiml@sece.ac.in
- Password: (your password)
- Monthly Income: 100000

Click "Create Account" - Should work now!

## Quick Commands Reference

### Start Backend (after Java + PostgreSQL installed)
```bash
cd backend
mvn spring-boot:run
```

### Start Frontend (already working)
```bash
cd frontend
npm run dev
```

### Start ML Service (optional, for predictions)
```bash
cd ml-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Troubleshooting

### "Java not found"
- Install Java 17 from link above
- Add to PATH: `C:\Program Files\Eclipse Adoptium\jdk-17.x.x\bin`
- Restart terminal

### "Connection refused to localhost:8080"
- Backend is not running
- Start backend with: `cd backend && mvn spring-boot:run`

### "Database connection failed"
- PostgreSQL not running: Start PostgreSQL service
- Database doesn't exist: Run CREATE DATABASE commands above
- Wrong credentials: Check .env file in backend folder

### "Port 8080 already in use"
```bash
# Find what's using port 8080
netstat -ano | findstr :8080

# Kill the process
taskkill /PID <PID> /F
```

## Current Status

✅ Frontend: Running on http://localhost:5173
❌ Backend: Not running (needs Java + PostgreSQL)
❌ ML Service: Not running (optional for now)

## Next Steps

1. Install Java 17
2. Install PostgreSQL 16
3. Create database (SQL commands above)
4. Run: `setup-backend.bat`
5. Try registration again

## Alternative: Use Demo Data

If you want to skip registration and just explore the UI, you can use demo credentials once backend is running:

```
Email: demo@finguard.ai
Password: Demo@123
```

(Note: Demo user needs to be seeded in database first)
