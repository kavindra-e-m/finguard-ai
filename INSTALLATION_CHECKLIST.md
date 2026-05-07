# FinGuard AI - Installation Checklist

## ✅ What I've Done For You

1. ✅ Opened Java 17 download page in your browser
2. ✅ Opened PostgreSQL download page in your browser
3. ✅ Created all configuration files (.env)
4. ✅ Set up Maven wrapper
5. ✅ Created automated setup scripts

## 📋 What You Need To Do

### Step 1: Install Java 17 (5 minutes)

From the browser tab that just opened:
1. Click "Download" for **Windows x64 MSI** (OpenJDK 17 LTS)
2. Run the downloaded `.msi` file
3. Click "Next" through the installer (use defaults)
4. Wait for installation to complete
5. Click "Finish"

**Verify:** Open new Command Prompt and type:
```cmd
java -version
```
Should show: `openjdk version "17.x.x"`

### Step 2: Install PostgreSQL 16 (5 minutes)

From the other browser tab:
1. Click "Download the installer"
2. Download PostgreSQL 16 for Windows x86-64
3. Run the downloaded `.exe` file
4. Click "Next" through the installer
5. **IMPORTANT:** When asked for password, enter: `postgres`
6. Keep port as: `5432`
7. Complete installation

### Step 3: Create Database (1 minute)

**Option A - Automatic:**
```cmd
setup-database.bat
```

**Option B - Manual (if Option A fails):**
1. Open pgAdmin (installed with PostgreSQL)
2. Connect to PostgreSQL (password: postgres)
3. Open Query Tool
4. Copy and paste contents of `setup-database.sql`
5. Click Execute

### Step 4: Start Backend (2 minutes)

```cmd
start-backend.bat
```

This will:
- Build the backend (first time takes 1-2 minutes)
- Start the server on port 8080

### Step 5: Test Registration

1. Go to http://localhost:5173
2. Click "Create Account"
3. Fill in your details:
   - Name: Kavindra
   - Email: kavindra.em2024aiml@sece.ac.in
   - Password: (your choice)
   - Monthly Income: 100000
4. Click "Create Account"

Should work now! ✅

## 🔧 Quick Commands

```cmd
# Setup database
setup-database.bat

# Start backend
start-backend.bat

# Start frontend (if not running)
cd frontend
npm run dev
```

## 🌐 Service URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8080 |
| Swagger API Docs | http://localhost:8080/swagger-ui.html |
| Health Check | http://localhost:8080/actuator/health |

## ❓ Troubleshooting

**Java not found after installation:**
- Close and reopen Command Prompt
- Or restart your computer

**PostgreSQL password error:**
- Use the password you set during installation
- Edit `setup-database.bat` to use your password

**Port 8080 already in use:**
```cmd
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

## 📞 Need Help?

If you encounter issues:
1. Check the error message
2. Verify Java 17 is installed: `java -version`
3. Verify PostgreSQL is running: Check Services
4. Check if database exists: Open pgAdmin
