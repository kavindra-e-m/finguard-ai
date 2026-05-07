# FinGuard AI - Installation Prerequisites

## Current System Status

✅ Node.js v25.2.1 - INSTALLED
❌ Java 17+ - NOT FOUND
❌ Python 3.11+ - NOT FOUND
❌ Docker - NOT FOUND
❌ PostgreSQL - NOT CHECKED

## Installation Steps

### 1. Install Java 17 (Required for Backend)

**Download:**
https://adoptium.net/temurin/releases/?version=17

**Steps:**
1. Download Windows x64 MSI installer
2. Run installer with default settings
3. Verify: Open new terminal and run `java -version`

### 2. Install Python 3.11+ (Required for ML Service)

**Download:**
https://www.python.org/downloads/

**Steps:**
1. Download Python 3.11 or higher
2. Run installer
3. ✅ CHECK "Add Python to PATH"
4. Click "Install Now"
5. Verify: Open new terminal and run `python --version`

### 3. Install PostgreSQL 16 (Required for Database)

**Download:**
https://www.postgresql.org/download/windows/

**Steps:**
1. Download PostgreSQL 16 installer
2. Run installer
3. Set password for postgres user
4. Keep default port 5432
5. After installation, create database:

```sql
-- Open pgAdmin or psql
CREATE DATABASE finguard_db;
CREATE USER finguard_user WITH PASSWORD 'finguard_pass';
GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;
```

### 4. Install Docker Desktop (Optional - for containerized deployment)

**Download:**
https://www.docker.com/products/docker-desktop/

**Steps:**
1. Download Docker Desktop for Windows
2. Run installer
3. Restart computer if prompted
4. Start Docker Desktop
5. Verify: `docker --version`

## Quick Start After Installation

### Option A: With All Prerequisites Installed

```bash
# Start all services
start-local.bat
```

### Option B: Frontend Only (Current)

```bash
# Start frontend only
start-frontend.bat
```

Then manually start backend and ML service in separate terminals.

### Option C: With Docker

```bash
# Start everything with Docker
docker-compose up --build
```

## Verify Installation

After installing prerequisites, run these commands:

```bash
java -version          # Should show Java 17+
python --version       # Should show Python 3.11+
node --version         # Should show Node.js 20+
psql --version         # Should show PostgreSQL 16+
docker --version       # Should show Docker version
```

## Next Steps

1. Install missing prerequisites from above
2. Run `start-local.bat` to start all services
3. Access frontend at http://localhost:5173
4. Register or use demo credentials:
   - Email: demo@finguard.ai
   - Password: Demo@123

## Minimal Setup (Frontend Only)

If you only want to see the frontend UI:

```bash
cd frontend
npm install
npm run dev
```

Note: Backend features won't work without Java and PostgreSQL.
