# FinGuard AI - Frontend, Backend & ML Integration Guide

## Architecture Overview

FinGuard AI is a three-tier microservices application:

```
┌─────────────────────────────────────────────────────────────────┐
│                       FRONTEND (React/Vite)                      │
│                       Port: 5173 (localhost)                     │
│  - UI Components (Dashboard, Expenses, Investments, etc.)       │
│  - API Client (Axios) with Auth Token Management                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    HTTP/REST API Calls
                         (axios)
                             │
        ┌────────────────────┴────────────────────┐
        │                                          │
┌───────▼──────────────────────┐    ┌────────────▼──────────────┐
│  BACKEND (Spring Boot Java)   │    │                            │
│  Port: 8080 (localhost)       │    │  ML SERVICE (FastAPI)      │
│  - REST Controllers           │    │  Port: 8000 (localhost)    │
│  - Authentication (JWT)       │    │  - ML Model Routes         │
│  - Business Logic             │    │  - Data Processing         │
│  - Database Integration       │    │  - Model Training          │
│  - ML Service Client          │    │                            │
└───────┬──────────────────────┘    └────────────┬───────────────┘
        │                                         │
        │                  HTTP/REST
        │                   (RestTemplate)
        └─────────────────────┬───────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  POSTGRESQL DB    │
                    │  Port: 5432       │
                    │  Database:        │
                    │  finguard_db      │
                    └───────────────────┘
```

## Component Details

### 1. Frontend (React + TypeScript + Vite)
**Location:** `/frontend`  
**Port:** 5173  
**Key Files:**
- `src/services/api.ts` - Axios client configuration
- `src/pages/` - Page components
- `src/store/authStore.ts` - Authentication state
- `vite.config.ts` - Build configuration

**API Services:**
- `authAPI` - Login/Register
- `expenseAPI` - Expense management
- `investmentAPI` - Investment management
- `analyticsAPI` - ML predictions

**Environment Variables:**
```env
VITE_API_URL=http://localhost:8080
VITE_ML_SERVICE_URL=http://localhost:8000
```

### 2. Backend (Spring Boot Java)
**Location:** `/backend`  
**Port:** 8080  
**Key Files:**
- `src/main/java/com/finguard/controller/` - REST Controllers
- `src/main/java/com/finguard/service/` - Business logic
- `src/main/java/com/finguard/security/` - JWT auth
- `pom.xml` - Dependencies
- `src/main/resources/application.properties` - Configuration

**Main Controllers:**
1. **AuthController** (`/api/auth`)
   ```
   POST   /register - User registration
   POST   /login    - User login
   ```

2. **ExpenseController** (`/api/expenses`)
   ```
   GET    /           - Get all expenses (paginated)
   POST   /           - Create expense
   GET    /summary    - Get expense summary
   GET    /{id}       - Get expense details
   DELETE /{id}       - Delete expense
   GET    /monthly-trend - Monthly trend analysis
   ```

3. **InvestmentController** (`/api/investments`)
   ```
   GET    /           - Get all investments
   POST   /           - Create investment
   GET    /summary    - Get investment summary
   POST   /optimize   - Portfolio optimization
   GET    /{id}       - Get investment details
   ```

4. **AnalyticsController** (`/api/analytics`)
   ```
   GET    /predict-expense      - Predict future expenses
   GET    /personality          - Detect personality type
   GET    /stress               - Predict financial stress
   GET    /financial-health     - Financial health score
   GET    /anomalies            - Detect anomalies
   ```

**ML Integration Points:**
- `MLService.java` - Calls ML microservice endpoints
- Uses `RestTemplate` for HTTP communication
- Handles data transformation between Java and Python

**Configuration:**
```properties
server.port=8080
spring.datasource.url=jdbc:postgresql://localhost:5432/finguard_db
ml.service.url=http://localhost:8000
cors.allowed-origins=http://localhost:5173
```

### 3. ML Service (FastAPI + Python)
**Location:** `/ml-service`  
**Port:** 8000  
**Key Files:**
- `main.py` - FastAPI app setup and routes
- `config.py` - Configuration
- `ml/` - ML model implementations
- `routes/` - API endpoints
- `schemas/` - Data validation

**API Routes:**
1. **GET** `/health` - Health check
2. **GET** `/` - Service info with loaded models

**ML Endpoints** (all under `/ml` prefix):

1. **Expense Prediction**
   ```
   POST /ml/predict-expense
   Input:
   {
     "user_id": 1,
     "monthly_expenses": [
       {"month": "2024-01-01", "amount": 1000},
       {"month": "2024-02-01", "amount": 1050}
     ]
   }
   Output:
   {
     "predicted_next_month": 1075,
     "confidence_lower": 950,
     "confidence_upper": 1200,
     "trend": "upward",
     "forecast_3_months": [1075, 1090, 1110]
   }
   ```

2. **Personality Detection**
   ```
   POST /ml/detect-personality
   Input:
   {
     "savings_ratio": 0.3,
     "expense_variability": 0.15,
     "investment_frequency": 2,
     "risk_exposure": 0.2,
     "food_ratio": 0.3,
     "entertainment_ratio": 0.1,
     "avg_transaction": 45.50,
     "monthly_income": 5000
   }
   Output:
   {
     "personality_type": "Cautious Saver",
     "confidence": 0.85,
     "probabilities": {
       "Cautious Saver": 0.85,
       "Balanced Manager": 0.12,
       "Risk Taker": 0.03
     },
     "description": "Personality description"
   }
   ```

3. **Stress Prediction**
   ```
   POST /ml/predict-stress
   Input: {financial features}
   Output:
   {
     "stress_level": "moderate",
     "confidence": 0.78,
     "risk_factors": [...]
   }
   ```

4. **Anomaly Detection**
   ```
   POST /ml/detect-anomalies
   Input: {expense data}
   Output:
   {
     "anomalies": [...],
     "threshold": 1500
   }
   ```

5. **Portfolio Optimization**
   ```
   POST /ml/optimize-portfolio
   Input:
   {
     "risk_tolerance": "moderate",
     "available_capital": 10000,
     "investment_horizon_years": 5
   }
   Output:
   {
     "recommended_allocation": {...},
     "expected_return": 0.07,
     "risk_level": 0.12
   }
   ```

6. **Financial Health Score**
   ```
   POST /ml/calculate-health-score
   Input: {financial metrics}
   Output:
   {
     "health_score": 72,
     "components": {...},
     "recommendations": [...]
   }
   ```

**Configuration:**
```python
DATABASE_URL=postgresql://finguard_user:finguard_pass@localhost:5432/finguard_db
MODEL_PATH=./models
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://localhost:8080
```

## Data Flow Examples

### Example 1: User Login Flow
```
1. Frontend: User enters credentials
   POST http://localhost:8080/api/auth/login
   Body: {email, password}

2. Backend: Validates credentials, generates JWT token
   Response: {token, user: {id, name, email, monthlyIncome}}

3. Frontend: Stores token in localStorage, makes authenticated requests
   Header: Authorization: Bearer <token>
```

### Example 2: Expense Prediction Flow
```
1. Frontend: User clicks "Predict Expenses"
   GET http://localhost:8080/api/analytics/predict-expense
   Header: Authorization: Bearer <token>

2. Backend AnalyticsController:
   - Identifies authenticated user
   - Calls AnalyticsService.predictExpense(userId)

3. AnalyticsService:
   - Queries database for last 12 months expenses
   - Formats data for ML service
   - Calls MLService.predictExpense(monthlyExpenses)

4. MLService (Java):
   - Makes HTTP POST to ML service
   POST http://localhost:8000/ml/predict-expense
   Body: {user_id, monthly_expenses}

5. ML Service (Python):
   - Loads ExpensePredictor model
   - Processes monthly expense data
   - Generates forecast with confidence intervals
   Response: {predicted_next_month, confidence_lower, confidence_upper, trend, forecast_3_months}

6. Backend:
   - Transforms response to ExpensePrediction DTO
   - Returns to frontend

7. Frontend:
   - Displays prediction with chart and recommendations
```

### Example 3: Personality Detection Flow
```
1. Frontend calls /api/analytics/personality

2. Backend AnalyticsService:
   - Retrieves user data and expenses
   - Calculates features:
     * savings_ratio
     * expense_variability
     * investment_frequency
     * risk_exposure
     * food_ratio
     * entertainment_ratio
     * avg_transaction
     * monthly_income

3. MLService calls ML microservice:
   POST http://localhost:8000/ml/detect-personality
   Body: {features}

4. ML Service uses trained classifier to predict personality type

5. Response flows back through chain to frontend
```

## Integration Checklist

### Prerequisites
- [ ] Java 17+ installed
- [ ] Node.js 20+ installed
- [ ] Python 3.11+ installed
- [ ] PostgreSQL 16 running on localhost:5432
- [ ] Database credentials: user=finguard_user, pass=finguard_pass, db=finguard_db

### Environment Setup
- [ ] Update root `.env` with localhost URLs (already done)
- [ ] Update `backend/src/main/resources/application.properties` if needed
- [ ] Update `ml-service/.env` with database credentials
- [ ] Create `frontend/.env` from `frontend/.env.example`

### Service Startup
- [ ] Start PostgreSQL database
- [ ] Start ML Service: `python -m uvicorn main:app --reload --port 8000`
- [ ] Start Backend: `./mvnw spring-boot:run`
- [ ] Start Frontend: `npm run dev`

### Database Setup
- [ ] Run database migrations
- [ ] Train ML models: `python ml/train_all_models.py`
- [ ] Seed sample data: `python data/seed_data.py`

### Testing Endpoints
- [ ] Test Backend health: `curl http://localhost:8080/health`
- [ ] Test ML Service health: `curl http://localhost:8000/health`
- [ ] Test Frontend access: `http://localhost:5173`
- [ ] Backend Swagger docs: `http://localhost:8080/swagger-ui.html`
- [ ] ML Service docs: `http://localhost:8000/docs`

### Feature Testing
- [ ] User registration working
- [ ] User login working
- [ ] Add expense working
- [ ] Add investment working
- [ ] Get expense predictions
- [ ] Get personality detection
- [ ] Get stress level prediction
- [ ] Get financial health score
- [ ] Get anomaly detection

## Common Issues & Troubleshooting

### Issue: ML Service returns 404 for routes
**Solution:**
- Check routes are registered in `main.py`
- Verify router prefixes match
- Check CORS configuration

### Issue: Backend can't call ML Service
**Solution:**
- Verify ML_SERVICE_URL in application.properties
- Check ML service is running on correct port
- Test connectivity: `curl http://localhost:8000/health`
- Check firewall rules

### Issue: Frontend getting CORS errors
**Solution:**
- Update CORS_ALLOWED_ORIGINS in backend properties
- Check frontend port matches CORS_ALLOWED_ORIGINS
- Verify API endpoints are correct

### Issue: Database connection fails
**Solution:**
- Ensure PostgreSQL is running
- Check database exists: `createdb finguard_db`
- Check user exists: `psql -U finguard_user`
- Verify credentials in .env and application.properties

### Issue: JWT token expired
**Solution:**
- JWT_EXPIRATION is in milliseconds (86400000 = 24 hours)
- Check system clock sync
- Clear localStorage and re-login

## API Documentation

### Accessing API Docs
- **Backend Swagger UI:** http://localhost:8080/swagger-ui.html
- **ML Service Docs:** http://localhost:8000/docs

### Authentication
All endpoints except `/auth/*` require JWT token in header:
```
Authorization: Bearer <jwt_token>
```

### Response Format
Standard JSON response:
```json
{
  "data": {...},
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "success"
}
```

## Development Tips

### Hot Reload
- **Frontend:** Vite provides hot reload during `npm run dev`
- **Backend:** Spring Boot Devtools provides auto-reload during `./mvnw spring-boot:run`
- **ML Service:** Use `--reload` flag with uvicorn

### For Debugging
- Backend logs: Check console output
- ML Service logs: Check `ml-service/logs/ml_service.log`
- Frontend: Use browser DevTools

### Testing JWT Tokens
```bash
# Get token from login response
TOKEN=$(curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' | jq -r '.data.token')

# Use token in subsequent requests
curl http://localhost:8080/api/analytics/predict-expense \
  -H "Authorization: Bearer $TOKEN"
```

## Production Deployment

For production, use Docker Compose:
```bash
docker-compose up --build
```

This will:
1. Start PostgreSQL database
2. Build and start ML Service
3. Build and start Backend
4. Build and start Frontend
5. Set up networking and volumes

All services communicate via internal Docker network.
