# FinGuard AI - Complete API Endpoints Reference

## Base URLs
- **Backend:** `http://localhost:8080`
- **ML Service:** `http://localhost:8000`
- **Frontend:** `http://localhost:5173`

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [Expense Endpoints](#expense-endpoints)
3. [Investment Endpoints](#investment-endpoints)
4. [Analytics/ML Endpoints](#analyticsml-endpoints)
5. [ML Service Direct Endpoints](#ml-service-direct-endpoints)
6. [System Health Endpoints](#system-health-endpoints)

---

## Authentication Endpoints

### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "Password123!",
  "monthlyIncome": 5000
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "monthlyIncome": 5000,
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Login User
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "Password123!"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "type": "Bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

---

## Expense Endpoints

All expense endpoints require authentication:
```
Authorization: Bearer <token>
```

### Get All Expenses (Paginated)
```http
GET /api/expenses?page=0&size=20
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "content": [
    {
      "id": 1,
      "userId": 1,
      "category": "FOOD",
      "amount": 45.50,
      "description": "Groceries",
      "expenseDate": "2024-01-15",
      "createdAt": "2024-01-15T10:30:00Z"
    }
  ],
  "page": 0,
  "size": 20,
  "totalElements": 150,
  "totalPages": 8
}
```

### Create Expense
```http
POST /api/expenses
Authorization: Bearer <token>
Content-Type: application/json

{
  "category": "FOOD",
  "amount": 45.50,
  "description": "Groceries",
  "expenseDate": "2024-01-15"
}
```

**Response (201):**
```json
{
  "id": 151,
  "userId": 1,
  "category": "FOOD",
  "amount": 45.50,
  "description": "Groceries",
  "expenseDate": "2024-01-15",
  "createdAt": "2024-01-15T10:35:00Z"
}
```

### Get Expense Details
```http
GET /api/expenses/{id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "userId": 1,
  "category": "FOOD",
  "amount": 45.50,
  "description": "Groceries",
  "expenseDate": "2024-01-15",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### Delete Expense
```http
DELETE /api/expenses/{id}
Authorization: Bearer <token>
```

**Response (204):** No content

### Get Expense Summary
```http
GET /api/expenses/summary
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "totalExpenses": 5000.00,
  "monthlyAverage": 1250.00,
  "byCategory": {
    "FOOD": 800.00,
    "TRANSPORT": 400.00,
    "ENTERTAINMENT": 300.00,
    "UTILITIES": 250.00,
    "CLOTHING": 200.00,
    "HEALTHCARE": 100.00,
    "OTHER": 1000.00
  },
  "percentageByCategory": {
    "FOOD": 16.0,
    "TRANSPORT": 8.0,
    "ENTERTAINMENT": 6.0,
    "UTILITIES": 5.0,
    "CLOTHING": 4.0,
    "HEALTHCARE": 2.0,
    "OTHER": 20.0
  }
}
```

### Get Monthly Trend
```http
GET /api/expenses/monthly-trend
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "months": [
    "2023-01",
    "2023-02",
    "2023-03",
    "2023-04",
    "2023-05",
    "2023-06"
  ],
  "amounts": [1200, 1150, 1300, 1250, 1280, 1210],
  "average": 1230,
  "trend": "stable",
  "percentChange": -0.83
}
```

### Expense Categories
Valid categories:
- `FOOD` - Groceries, dining out
- `TRANSPORT` - Gas, public transport, maintenance
- `ENTERTAINMENT` - Movies, games, hobbies
- `UTILITIES` - Electricity, water, internet
- `CLOTHING` - Apparel, accessories
- `HEALTHCARE` - Medical, medicines
- `OTHER` - Miscellaneous

---

## Investment Endpoints

All investment endpoints require authentication:
```
Authorization: Bearer <token>
```

### Get All Investments
```http
GET /api/investments
Authorization: Bearer <token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "userId": 1,
    "investmentType": "STOCKS",
    "amount": 10000.00,
    "expectedReturn": 8.5,
    "investmentDate": "2023-06-15",
    "createdAt": "2023-06-15T10:30:00Z"
  },
  {
    "id": 2,
    "userId": 1,
    "investmentType": "BONDS",
    "amount": 5000.00,
    "expectedReturn": 4.0,
    "investmentDate": "2023-09-20",
    "createdAt": "2023-09-20T14:20:00Z"
  }
]
```

### Create Investment
```http
POST /api/investments
Authorization: Bearer <token>
Content-Type: application/json

{
  "investmentType": "STOCKS",
  "amount": 10000,
  "expectedReturn": 8.5,
  "investmentDate": "2024-01-15"
}
```

**Response (201):**
```json
{
  "id": 3,
  "userId": 1,
  "investmentType": "STOCKS",
  "amount": 10000.00,
  "expectedReturn": 8.5,
  "investmentDate": "2024-01-15",
  "createdAt": "2024-01-15T10:35:00Z"
}
```

### Get Investment Details
```http
GET /api/investments/{id}
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "userId": 1,
  "investmentType": "STOCKS",
  "amount": 10000.00,
  "expectedReturn": 8.5,
  "investmentDate": "2023-06-15",
  "createdAt": "2023-06-15T10:30:00Z"
}
```

### Get Investment Summary
```http
GET /api/investments/summary
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "totalInvested": 15000.00,
  "byType": {
    "STOCKS": 10000.00,
    "BONDS": 5000.00,
    "MUTUAL_FUNDS": 0.00,
    "CRYPTO": 0.00,
    "COMMODITIES": 0.00,
    "REAL_ESTATE": 0.00
  },
  "expectedAnnualReturn": 925.00,
  "diversificationScore": 7.5
}
```

### Optimize Portfolio
```http
POST /api/investments/optimize
Authorization: Bearer <token>
Content-Type: application/json

{
  "riskTolerance": "moderate",
  "availableCapital": 5000,
  "investmentHorizonYears": 5
}
```

**Response (200):**
```json
{
  "recommendedAllocation": {
    "stocks": 40,
    "bonds": 35,
    "mutualFunds": 15,
    "crypto": 5,
    "commodities": 5
  },
  "expectedAnnualReturn": 0.065,
  "riskLevel": 0.12,
  "sharpeRatio": 0.54,
  "allocations": [
    {
      "assetClass": "stocks",
      "percentage": 40,
      "amount": 2000,
      "expectedReturn": 0.08
    }
  ]
}
```

### Investment Types
Valid types:
- `STOCKS` - Individual company stocks
- `BONDS` - Fixed income securities
- `MUTUAL_FUNDS` - Managed funds
- `CRYPTO` - Cryptocurrencies
- `COMMODITIES` - Metals, oil, etc.
- `REAL_ESTATE` - Property investments

---

## Analytics/ML Endpoints

All analytics endpoints require authentication and call ML service:
```
Authorization: Bearer <token>
```

### Predict Expenses (ML)
```http
GET /api/analytics/predict-expense
Authorization: Bearer <token>
```

**Backend Flow:**
1. Backend retrieves last 12 months of expense data
2. Calls ML service: `POST http://localhost:8000/ml/predict-expense`
3. Returns formatted prediction

**Response (200):**
```json
{
  "predictedNextMonth": 1250.50,
  "confidenceLower": 1100.00,
  "confidenceUpper": 1400.00,
  "trend": "upward",
  "forecast3Months": [1250.50, 1280.00, 1310.00]
}
```

### Detect Personality (ML)
```http
GET /api/analytics/personality
Authorization: Bearer <token>
```

**Backend Flow:**
1. Backend calculates financial features from user expenses
2. Calls ML service: `POST http://localhost:8000/ml/detect-personality`
3. Returns personality analysis

**Response (200):**
```json
{
  "personalityType": "Cautious Saver",
  "confidence": 0.87,
  "probabilities": {
    "Cautious Saver": 0.87,
    "Balanced Manager": 0.10,
    "Risk Taker": 0.03
  },
  "description": "You are a financially conservative person...",
  "recommendations": [
    "Consider diversifying investments",
    "Build emergency fund",
    "Review insurance coverage"
  ]
}
```

### Predict Stress Level (ML)
```http
GET /api/analytics/stress
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "stressLevel": "moderate",
  "riskScore": 6.5,
  "confidence": 0.78,
  "factors": {
    "debt_to_income_ratio": 0.25,
    "savings_rate": 0.30,
    "expense_growth": 0.05
  },
  "recommendations": [
    "Reduce high-interest debt",
    "Increase emergency fund to 6 months",
    "Review expense growth"
  ]
}
```

### Calculate Financial Health (ML)
```http
GET /api/analytics/financial-health
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "overallScore": 72,
  "grade": "B",
  "scoreBreakdown": {
    "expenses": 80,
    "savings": 65,
    "investments": 75,
    "debt": 60
  },
  "recommendations": [
    "Increase savings rate",
    "Reduce high-interest debt",
    "Diversify investments"
  ],
  "healthStatus": "good"
}
```

### Detect Anomalies (ML)
```http
GET /api/analytics/anomalies
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "anomalies": [
    {
      "id": 15,
      "category": "ENTERTAINMENT",
      "amount": 500.00,
      "date": "2024-01-10",
      "reason": "Amount 4x higher than average for this category"
    }
  ],
  "totalAnomalies": 1,
  "threshold": 300.00,
  "anomalyPercentage": 0.67
}
```

---

## ML Service Direct Endpoints

These endpoints are called internally by backend but can also be called directly:

### Health Check
```http
GET http://localhost:8000/health
```

**Response (200):**
```json
{
  "status": "healthy",
  "models_loaded": 3,
  "service": "ml-service"
}
```

### Service Info
```http
GET http://localhost:8000/
```

**Response (200):**
```json
{
  "service": "FinGuard AI ML Service",
  "version": "1.0.0",
  "status": "running",
  "loaded_models": [
    "personality_detector",
    "stress_predictor",
    "anomaly_detector"
  ]
}
```

### Predict Expenses (Direct)
```http
POST http://localhost:8000/ml/predict-expense
Content-Type: application/json

{
  "user_id": 1,
  "monthly_expenses": [
    {"month": "2023-07-01", "amount": 1200},
    {"month": "2023-08-01", "amount": 1150},
    {"month": "2023-09-01", "amount": 1300},
    {"month": "2023-10-01", "amount": 1250},
    {"month": "2023-11-01", "amount": 1280},
    {"month": "2023-12-01", "amount": 1210}
  ]
}
```

**Response (200):**
```json
{
  "predicted_next_month": 1250.50,
  "confidence_lower": 1100.00,
  "confidence_upper": 1400.00,
  "trend": "upward",
  "forecast_3_months": [1250.50, 1280.00, 1310.00]
}
```

### Detect Personality (Direct)
```http
POST http://localhost:8000/ml/detect-personality
Content-Type: application/json

{
  "savings_ratio": 0.30,
  "expense_variability": 0.15,
  "investment_frequency": 2,
  "risk_exposure": 0.20,
  "food_ratio": 0.30,
  "entertainment_ratio": 0.10,
  "avg_transaction": 45.50,
  "monthly_income": 5000
}
```

**Response (200):**
```json
{
  "personality_type": "Cautious Saver",
  "confidence": 0.87,
  "probabilities": {
    "Cautious Saver": 0.87,
    "Balanced Manager": 0.10,
    "Risk Taker": 0.03
  },
  "description": "You focus on long-term security..."
}
```

### Predict Stress (Direct)
```http
POST http://localhost:8000/ml/predict-stress
Content-Type: application/json

{
  "debt_to_income_ratio": 0.25,
  "savings_rate": 0.30,
  "expense_growth_rate": 0.05,
  "income_stability_score": 0.85,
  "emergency_fund_months": 3
}
```

**Response (200):**
```json
{
  "risk_score": 6.5,
  "risk_label": "moderate",
  "confidence": 0.78,
  "risk_factors": [
    "Debt level moderate",
    "Savings rate could be higher"
  ],
  "recommendations": [
    "Increase emergency fund to 6 months",
    "Focus on debt reduction"
  ]
}
```

### Optimize Portfolio (Direct)
```http
POST http://localhost:8000/ml/optimize-portfolio
Content-Type: application/json

{
  "risk_tolerance": "moderate",
  "available_capital": 10000,
  "investment_horizon_years": 5
}
```

**Response (200):**
```json
{
  "recommended_allocation": {
    "stocks": 40,
    "bonds": 35,
    "mutual_funds": 15,
    "crypto": 5,
    "commodities": 5
  },
  "expected_annual_return": 0.065,
  "risk_level": 0.12,
  "sharpe_ratio": 0.54,
  "allocations": [
    {
      "asset_class": "stocks",
      "percentage": 40,
      "amount": 4000,
      "expected_return": 0.08
    }
  ]
}
```

### Calculate Financial Health (Direct)
```http
POST http://localhost:8000/ml/financial-health-score
Content-Type: application/json

{
  "monthly_income": 5000,
  "monthly_expenses": 1500,
  "total_savings": 15000,
  "total_debt": 5000,
  "monthly_investments": 500,
  "emergency_fund": 10000,
  "expense_trend_3m": 0.05,
  "age": 35
}
```

**Response (200):**
```json
{
  "overall_score": 72,
  "grade": "B",
  "score_breakdown": {
    "expense_ratio": 80,
    "savings_rate": 65,
    "investment_score": 75,
    "debt_ratio": 60,
    "emergency_fund": 85
  },
  "recommendations": [
    "Increase savings rate",
    "Reduce debt load",
    "Diversify investments"
  ],
  "health_status": "good"
}
```

### Detect Anomalies (Direct)
```http
POST http://localhost:8000/ml/detect-anomalies
Content-Type: application/json

{
  "user_id": 1,
  "expenses": [
    {"id": 1, "category": "FOOD", "amount": 50, "date": "2024-01-10"},
    {"id": 2, "category": "ENTERTAINMENT", "amount": 500, "date": "2024-01-11"},
    {"id": 3, "category": "FOOD", "amount": 45, "date": "2024-01-12"}
  ]
}
```

**Response (200):**
```json
{
  "anomalies": [
    {
      "id": 2,
      "category": "ENTERTAINMENT",
      "amount": 500,
      "date": "2024-01-11",
      "anomaly_score": 0.92,
      "reason": "4x higher than typical for this category"
    }
  ],
  "total_anomalies": 1,
  "total_transactions": 3,
  "anomaly_percentage": 33.33,
  "threshold": 150.0
}
```

---

## System Health Endpoints

### Backend Health
```http
GET http://localhost:8080/actuator/health
```

**Response (200):**
```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP"
    },
    "livenessState": {
      "status": "UP"
    },
    "readinessState": {
      "status": "UP"
    }
  }
}
```

### ML Service Health
```http
GET http://localhost:8000/health
```

**Response (200):**
```json
{
  "status": "healthy",
  "models_loaded": 3,
  "service": "ml-service"
}
```

---

## Common Error Responses

### 400 Bad Request
```json
{
  "status": 400,
  "error": "Bad Request",
  "message": "Invalid request parameters",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 401 Unauthorized
```json
{
  "status": 401,
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 404 Not Found
```json
{
  "status": 404,
  "error": "Not Found",
  "message": "Resource not found",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 500 Internal Server Error
```json
{
  "status": 500,
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding:
- Per-user rate limits (e.g., 1000 requests/hour)
- Per-endpoint rate limits
- Sliding window or token bucket algorithms

---

## Pagination

Endpoints with pagination support these parameters:
- `page` - Page number (0-indexed, default: 0)
- `size` - Page size (default: 20, max: 100)
- `sort` - Sort field (e.g., `createdAt,desc`)

Example:
```
GET /api/expenses?page=2&size=50&sort=expenseDate,desc
```

---

## Frontend Integration

The frontend wraps all backend calls through `src/services/api.ts`:

```typescript
// Example usage in React component
import { analyticsAPI } from '@/services/api';

export function DashboardPage() {
  const [prediction, setPrediction] = useState(null);
  
  useEffect(() => {
    analyticsAPI.predictExpense()
      .then(res => setPrediction(res.data))
      .catch(err => console.error('Prediction failed', err));
  }, []);
  
  return <div>{/* Display prediction */}</div>;
}
```

---

## Testing with cURL

### Get Token
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@example.com",
    "password":"password"
  }' | jq '.data.token' --raw-output > token.txt

set TOKEN=<paste_token_here>
```

### Test Prediction
```bash
curl http://localhost:8080/api/analytics/predict-expense \
  -H "Authorization: Bearer %TOKEN%"
```

### Test ML Service Directly
```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/ml/predict-expense \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "monthly_expenses": [
      {"month": "2023-01-01", "amount": 1000}
    ]
  }'
```

---

## Documentation Tools

- **Backend Swagger UI:** http://localhost:8080/swagger-ui.html
- **ML Service Docs:** http://localhost:8000/docs
- **ML Service Alt Docs:** http://localhost:8000/redoc
