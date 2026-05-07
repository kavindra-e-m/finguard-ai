# FinGuard AI - Intelligent Financial Assistance & Investment Platform

![FinGuard AI](https://img.shields.io/badge/FinGuard-AI-blue)
![React](https://img.shields.io/badge/React-18-61DAFB)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.0-6DB33F)
![Python](https://img.shields.io/badge/Python-3.11-3776AB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)

FinGuard AI is a production-ready, research-grade intelligent financial platform that combines Data Science, Machine Learning, and Full Stack Web Development. Built on academic FinTech research foundations, it fills critical gaps in existing financial technology solutions.

## Key Features

### Core Capabilities
- **Expense Tracking & Management** - Log, categorize, and analyze all expenses
- **Financial Health Scoring** - AI-powered comprehensive financial wellness assessment
- **Expense Prediction** - Prophet-based forecasting for future expenses
- **Personality Detection** - ML classifier identifies financial behavior patterns (Conservative, Balanced, Aggressive, Impulsive)
- **Stress Prediction** - Early warning system for financial distress
- **Investment Portfolio Optimization** - Markowitz Mean-Variance optimization
- **Anomaly Detection** - Automatic flagging of unusual transactions

### Advanced Features
- **Monte Carlo Retirement Simulation** - 1000-run simulation for retirement planning
- **CSV Bank Statement Import** - Auto-categorize transactions from bank statements
- **Emotional Spending Detector** - Identify behavioral spending patterns
- **Financial Goal Tracker** - ML-powered goal achievability prediction

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FinGuard AI Platform                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │
│  │   React + Vite  │    │  Spring Boot 3  │    │   Python FastAPI ML     │ │
│  │   Frontend      │◄──►│   Backend       │◄──►│   Microservice          │ │
│  │   Port: 5173    │    │   Port: 8080    │    │   Port: 8000            │ │
│  │                 │    │                 │    │                         │ │
│  │ • TypeScript    │    │ • Java 17       │    │ • Prophet Forecasting   │ │
│  │ • Redux Toolkit │    │ • JWT Security  │    │ • Random Forest         │ │
│  │ • Recharts      │    │ • JPA/Hibernate │    │ • Logistic Regression   │ │
│  │ • Tailwind CSS  │    │ • REST APIs     │    │ • Portfolio Optimization│ │
│  │ • shadcn/ui     │    │ • Swagger Docs  │    │ • Isolation Forest      │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘ │
│           ▲                      ▲                      ▲                  │
│           │                      │                      │                  │
│           └──────────────────────┴──────────────────────┘                  │
│                                  │                                          │
│                         ┌─────────────────┐                                │
│                         │   PostgreSQL    │                                │
│                         │   Port: 5432    │                                │
│                         └─────────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React 18 + Vite + TypeScript | UI Framework |
| Frontend | Tailwind CSS + shadcn/ui | Styling & Components |
| Frontend | Redux Toolkit | State Management |
| Frontend | Recharts | Data Visualization |
| Backend | Spring Boot 3 + Java 17 | API Server |
| Backend | Spring Security + JWT | Authentication |
| Backend | JPA/Hibernate | ORM |
| ML Service | FastAPI + Python 3.11 | ML Microservice |
| ML Service | Prophet, scikit-learn, XGBoost | ML Models |
| ML Service | PyPortfolioOpt | Portfolio Optimization |
| Database | PostgreSQL 16 | Data Storage |
| DevOps | Docker + Docker Compose | Containerization |

## Prerequisites

- **Java 17** or higher
- **Python 3.11** or higher
- **Node.js 20** or higher
- **Docker** and **Docker Compose**
- **PostgreSQL** (if running locally)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/finguard-ai.git
cd finguard-ai
```

### 2. Environment Configuration

```bash
# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp ml-service/.env.example ml-service/.env
```

### 3. Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Train ML Models

```bash
# Execute training script in ML service container
docker exec finguard-ml-service python ml/train_all_models.py
```

### 5. Seed Demo Data

```bash
# Generate demo user and sample data
docker exec finguard-ml-service python data/seed_data.py
```

### 6. Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | React Application |
| Backend API | http://localhost:8080 | Spring Boot REST API |
| Backend Swagger | http://localhost:8080/swagger-ui.html | API Documentation |
| ML Service | http://localhost:8000 | FastAPI Health Check |
| ML Service Docs | http://localhost:8000/docs | FastAPI Swagger UI |

## Demo Credentials

```
Email: demo@finguard.ai
Password: Demo@123
```

## 📚 Integration Documentation

Complete documentation for the Frontend, Backend, and ML Service integration is available:

| Documentation | Purpose |
|---|---|
| [**INTEGRATION_COMPLETE.md**](./INTEGRATION_COMPLETE.md) | **START HERE** - Overview of complete integration setup |
| [**INTEGRATION_GUIDE.md**](./INTEGRATION_GUIDE.md) | Detailed architecture, data flows, and integration checklist |
| [**LOCAL_DEVELOPMENT.md**](./LOCAL_DEVELOPMENT.md) | Step-by-step local development setup and testing |
| [**API_REFERENCE.md**](./API_REFERENCE.md) | Complete API endpoint reference with examples |

### Integration Architecture

```
Frontend (React)
    ↓ API Calls (Axios + JWT Auth)
Backend (Spring Boot)
    ↓ ML Feature Extraction
ML Service (FastAPI)
    ↓ ML Models (Prophet, Random Forest, etc.)
Response Flow Back to Frontend
```

### Key Integration Points

- ✅ **Frontend → Backend**: REST API with JWT authentication
- ✅ **Backend → ML Service**: Internal HTTP calls for ML predictions
- ✅ **Database Integration**: PostgreSQL with JPA/Hibernate ORM
- ✅ **Real-time Analytics**: 5 ML-powered prediction endpoints
- ✅ **Secure Authentication**: JWT tokens with role-based access

### Verification

To verify all services are integrated correctly:

```bash
# Windows PowerShell
.\verify-integration.ps1

# Or manually check each service
curl http://localhost:5173     # Frontend
curl http://localhost:8080/actuator/health    # Backend
curl http://localhost:8000/health             # ML Service
```

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login and get JWT token |

### Expense Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/expenses | Create new expense |
| GET | /api/expenses | List all expenses (paginated) |
| GET | /api/expenses/summary | Get expense summary |
| GET | /api/expenses/monthly-trend | Get monthly trend data |
| DELETE | /api/expenses/{id} | Delete expense |

### Analytics Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/analytics/predict-expense | Predict next month expenses |
| GET | /api/analytics/personality | Detect financial personality |
| GET | /api/analytics/stress | Predict financial stress |
| GET | /api/analytics/financial-health | Get financial health score |
| GET | /api/analytics/anomalies | Detect anomalous transactions |

### Investment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/investments | Create investment |
| GET | /api/investments | List investments |
| POST | /api/investments/optimize | Get optimized portfolio |

## ML Models

| Model | Algorithm | Purpose | Input Features |
|-------|-----------|---------|----------------|
| Expense Predictor | Prophet + Linear Regression | Forecast future expenses | 12+ months historical data |
| Personality Detector | Random Forest | Classify financial behavior | 8 behavioral features |
| Stress Predictor | Logistic Regression | Predict financial distress | 5 financial health metrics |
| Portfolio Optimizer | Markowitz Mean-Variance | Optimize asset allocation | Risk tolerance, capital |
| Anomaly Detector | Isolation Forest | Detect unusual transactions | Amount, category, timing |
| Health Scorer | Rule-based + ML | Calculate financial wellness | Income, expenses, savings, debt |

## Project Structure

```
finguard-ai/
├── README.md
├── docker-compose.yml
├── .env.example
│
├── frontend/                    # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── store/               # Redux store
│   │   ├── hooks/               # Custom hooks
│   │   └── types/               # TypeScript types
│   └── ...
│
├── backend/                     # Spring Boot 3 + Java 17
│   └── src/
│       ├── config/              # Configuration classes
│       ├── controller/          # REST controllers
│       ├── service/             # Business logic
│       ├── repository/          # JPA repositories
│       ├── model/               # Entity classes
│       ├── dto/                 # Data transfer objects
│       └── security/            # JWT security
│
└── ml-service/                  # Python FastAPI ML Service
    ├── ml/                      # ML model implementations
    ├── routes/                  # API routes
    ├── schemas/                 # Pydantic schemas
    └── data/                    # Data generation scripts
```

## Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Backend Development

```bash
cd backend
./mvnw spring-boot:run
```

### ML Service Development

```bash
cd ml-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing

```bash
# Run backend tests
cd backend
./mvnw test

# Test ML endpoints
curl -X POST http://localhost:8000/ml/predict-expense \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "monthly_expenses": [...]}'
```

## Screenshots

### Dashboard
- Financial health score gauge
- Monthly expense trend chart
- Category breakdown pie chart
- Stress alerts and personality badge

### Expenses Page
- Add/edit expense form
- Expense table with pagination
- Category filtering
- Anomaly indicators

### Predictions Page
- Expense forecast chart
- Personality analysis card
- Stress level indicator
- Financial health breakdown

### Investments Page
- Portfolio allocation donut chart
- Investment form
- Optimization results
- Risk-return metrics

## Future Scope

- [ ] Multi-currency support
- [ ] Bank API integrations (Plaid, Yodlee)
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Advanced tax optimization
- [ ] Social features (family accounts)
- [ ] AI-powered chatbot advisor
- [ ] Cryptocurrency portfolio tracking

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Academic research foundation on digital wallet technology acceptance
- Prophet library by Facebook for time series forecasting
- PyPortfolioOpt for portfolio optimization algorithms
- Spring Boot and React communities for excellent documentation

## Support

For support, email support@finguard.ai or join our Slack channel.

---

**FinGuard AI** - Your Intelligent Financial Guardian 🛡️💰
