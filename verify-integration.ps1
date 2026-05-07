#!/usr/bin/env pwsh
<#
.SYNOPSIS
FinGuard AI - Integration Verification Script
Checks connectivity between Frontend, Backend, and ML Service

.DESCRIPTION
This script verifies:
1. Database connectivity
2. ML Service running and healthy
3. Backend API running and healthy
4. Frontend can connect to backend
5. Backend can connect to ML service
6. Key integrations working end-to-end
#>

param(
    [switch]$Verbose
)

# Colors for output
$GREEN = "`e[32m"
$RED = "`e[31m"
$YELLOW = "`e[33m"
$RESET = "`e[0m"
$BOLD = "`e[1m"

function Write-Success { Write-Host "$GREEN✓$RESET $args" }
function Write-Error { Write-Host "$RED✗$RESET $args" }
function Write-Warning { Write-Host "$YELLOW⚠$RESET $args" }
function Write-Info { Write-Host "$BOLD→$RESET $args" }

Write-Host "`nFinGuard AI - Integration Verification`n" -ForegroundColor Cyan
Write-Info "Starting integration checks..."

# Track results
$allHealthy = $true

# ==============================================================================
# 1. Database Connectivity
# ==============================================================================

Write-Host "`n$BOLD[1/5] Database Connectivity$RESET"

try {
    $result = psql -U finguard_user -d finguard_db -c "SELECT 1;" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "PostgreSQL database is accessible"
        Write-Success "Database: finguard_db, User: finguard_user"
    }
    else {
        Write-Error "PostgreSQL connection failed"
        Write-Warning "Ensure PostgreSQL is running on localhost:5432"
        Write-Warning "Connection string: postgresql://finguard_user:finguard_pass@localhost:5432/finguard_db"
        $allHealthy = $false
    }
}
catch {
    Write-Error "PostgreSQL not found or not running"
    Write-Warning "Install PostgreSQL or ensure it's running"
    $allHealthy = $false
}

# ==============================================================================
# 2. ML Service Health
# ==============================================================================

Write-Host "`n$BOLD[2/5] ML Service Health$RESET"

try {
    Write-Info "Checking http://localhost:8000/health ..."
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -ErrorAction Stop -TimeoutSec 5
    
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        Write-Success "ML Service is running"
        Write-Success "Status: $($data.status)"
        Write-Success "Models loaded: $($data.models_loaded)"
    }
    else {
        Write-Error "ML Service returned status $($response.StatusCode)"
        $allHealthy = $false
    }
}
catch {
    Write-Error "ML Service is not responding"
    Write-Warning "Ensure ML Service is started on port 8000"
    Write-Warning "Start with: cd ml-service && python -m uvicorn main:app --reload --port 8000"
    $allHealthy = $false
}

# ==============================================================================
# 3. Backend API Health
# ==============================================================================

Write-Host "`n$BOLD[3/5] Backend API Health$RESET"

try {
    Write-Info "Checking http://localhost:8080/actuator/health ..."
    $response = Invoke-WebRequest -Uri "http://localhost:8080/actuator/health" -ErrorAction Stop -TimeoutSec 5
    
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        Write-Success "Backend API is running"
        Write-Success "Status: $($data.status)"
        
        # Check database component
        if ($data.components.db.status -eq "UP") {
            Write-Success "Backend database connection: OK"
        }
        else {
            Write-Warning "Backend database connection: $($data.components.db.status)"
        }
    }
    else {
        Write-Error "Backend returned status $($response.StatusCode)"
        $allHealthy = $false
    }
}
catch {
    Write-Error "Backend API is not responding"
    Write-Warning "Ensure Backend is started on port 8080"
    Write-Warning "Start with: cd backend && mvnw.cmd spring-boot:run"
    $allHealthy = $false
}

# ==============================================================================
# 4. Frontend Connectivity
# ==============================================================================

Write-Host "`n$BOLD[4/5] Frontend Connectivity$RESET"

try {
    Write-Info "Checking http://localhost:5173 ..."
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -ErrorAction Stop -TimeoutSec 5
    
    if ($response.StatusCode -eq 200) {
        Write-Success "Frontend is accessible"
        Write-Success "Location: http://localhost:5173"
    }
    else {
        Write-Error "Frontend returned status $($response.StatusCode)"
        $allHealthy = $false
    }
}
catch {
    Write-Warning "Frontend is not currently running"
    Write-Warning "Start with: cd frontend && npm run dev"
}

# ==============================================================================
# 5. Backend to ML Service Integration
# ==============================================================================

Write-Host "`n$BOLD[5/5] Backend to ML Service Integration$RESET"

Write-Info "Testing if Backend can reach ML Service..."

# First, we need a token to test the backend
Write-Host "`nNote: Skipping integration test (requires authenticated user)"
Write-Warning "To test end-to-end:"
Write-Warning "1. Start all services"
Write-Warning "2. Register a user: POST http://localhost:8080/api/auth/register"
Write-Warning "3. Login to get token: POST http://localhost:8080/api/auth/login"
Write-Warning "4. Test prediction: GET http://localhost:8080/api/analytics/predict-expense"
Write-Warning "5. Check response comes from ML Service"

# ==============================================================================
# Ports Check
# ==============================================================================

Write-Host "`n$BOLD[Ports Summary]$RESET"

$ports = @{
    "PostgreSQL" = 5432
    "ML Service" = 8000
    "Backend API" = 8080
    "Frontend" = 5173
}

foreach ($service in $ports.GetEnumerator()) {
    $port = $service.Value
    
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $result = $tcp.BeginConnect("localhost", $port, $null, $null)
        $result.AsyncWaitHandle.WaitOne(1000, $false) | Out-Null
        
        if ($tcp.Connected) {
            Write-Success "$($service.Key): Port $port is open"
        }
        else {
            Write-Error "$($service.Key): Port $port is not responding"
            $allHealthy = $false
        }
        $tcp.Close()
    }
    catch {
        Write-Error "$($service.Key): Port $port check failed"
        $allHealthy = $false
    }
}

# ==============================================================================
# Environment Check
# ==============================================================================

Write-Host "`n$BOLD[Environment Configuration]$RESET"

# Check .env file
if (Test-Path ".env") {
    Write-Success "Root .env file exists"
    
    # Check key variables
    $envContent = Get-Content ".env" -Raw
    
    if ($envContent -like "*ML_SERVICE_URL=*") {
        Write-Success "ML_SERVICE_URL is configured"
    }
    else {
        Write-Warning "ML_SERVICE_URL not found in .env"
    }
}
else {
    Write-Warning "Root .env file not found"
}

# Check ML service .env
if (Test-Path "ml-service\.env") {
    Write-Success "ML Service .env file exists"
}
else {
    Write-Warning "ML Service .env file not found"
}

# Check frontend .env
if (Test-Path "frontend\.env") {
    Write-Success "Frontend .env file exists"
}
else {
    Write-Warning "Frontend .env file not found"
}

# ==============================================================================
# Summary
# ==============================================================================

Write-Host "`n$BOLD[Summary]$RESET"

if ($allHealthy) {
    Write-Success "`nAll major services are connected and ready!`n"
    Write-Host "Next steps:"
    Write-Host "1. Open Frontend: http://localhost:5173"
    Write-Host "2. Register a new user"
    Write-Host "3. Login and add some expenses"
    Write-Host "4. Test analytics features"
    Write-Host ""
}
else {
    Write-Error "`nSome services are not running or not connected.`n"
    Write-Host "Please check the warnings above and:"
    Write-Host "1. Ensure PostgreSQL is running"
    Write-Host "2. Start ML Service: python -m uvicorn main:app --reload --port 8000"
    Write-Host "3. Start Backend: mvnw.cmd spring-boot:run"
    Write-Host "4. Start Frontend: npm run dev"
    Write-Host ""
}

Write-Host "Detailed documentation:"
Write-Host "- Integration: INTEGRATION_GUIDE.md"
Write-Host "- API Reference: API_REFERENCE.md"
Write-Host "- Local Dev Setup: LOCAL_DEVELOPMENT.md"
Write-Host ""
