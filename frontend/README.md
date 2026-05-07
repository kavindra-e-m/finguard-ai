# FinGuard AI - Frontend

![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6?logo=typescript)
![Vite](https://img.shields.io/badge/Vite-7.2-646CFF?logo=vite)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38B2AC?logo=tailwind-css)

Modern, responsive frontend for FinGuard AI - An intelligent financial assistance and investment platform.

## 🚀 Live Demo

**Repository:** [https://github.com/kavindra-e-m/FG-front](https://github.com/kavindra-e-m/FG-front)

## ✨ Features

- 📊 **Interactive Dashboard** - Real-time financial health visualization
- 💰 **Expense Tracking** - Log and categorize expenses with ease
- 📈 **Predictions & Analytics** - AI-powered financial forecasting
- 💼 **Investment Portfolio** - Track and optimize investments
- 🎨 **Modern UI** - Built with shadcn/ui and Tailwind CSS
- 🔐 **Secure Authentication** - JWT-based auth with protected routes
- 📱 **Responsive Design** - Works seamlessly on all devices

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **React 18** | UI Framework |
| **TypeScript** | Type Safety |
| **Vite** | Build Tool & Dev Server |
| **Tailwind CSS** | Styling |
| **shadcn/ui** | UI Components |
| **Zustand** | State Management |
| **Axios** | HTTP Client |
| **Recharts** | Data Visualization |
| **React Router** | Routing |

## 📋 Prerequisites

- Node.js 20+ 
- npm or yarn
- Backend API running on `http://localhost:8080`

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kavindra-e-m/FG-front.git
cd FG-front
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8080
VITE_ML_SERVICE_URL=http://localhost:8000
VITE_APP_NAME=FinGuard AI
VITE_APP_VERSION=1.0.0
```

### 4. Start Development Server

```bash
npm run dev
```

The app will be available at: **http://localhost:5173**

## 📦 Build for Production

```bash
npm run build
```

Build output will be in the `dist/` directory.

## 🏗️ Project Structure

```
FG-front/
├── src/
│   ├── components/
│   │   ├── layout/          # Layout components (Navbar, Sidebar)
│   │   └── ui/              # shadcn/ui components
│   ├── pages/               # Page components
│   │   ├── DashboardPage.tsx
│   │   ├── ExpensesPage.tsx
│   │   ├── InvestmentsPage.tsx
│   │   ├── PredictionsPage.tsx
│   │   ├── LoginPage.tsx
│   │   └── RegisterPage.tsx
│   ├── services/            # API services
│   │   └── api.ts
│   ├── store/               # State management
│   │   └── authStore.ts
│   ├── types/               # TypeScript types
│   ├── hooks/               # Custom hooks
│   ├── lib/                 # Utilities
│   ├── App.tsx              # Main app component
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── .env.example             # Environment template
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
└── package.json             # Dependencies
```

## 🔌 API Integration

The frontend connects to the backend API at `http://localhost:8080/api`

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/login` | POST | User login |
| `/auth/register` | POST | User registration |
| `/expenses` | GET/POST/DELETE | Expense management |
| `/expenses/summary` | GET | Expense summary |
| `/analytics/*` | GET | Analytics & predictions |
| `/investments` | GET/POST | Investment management |
| `/investments/optimize` | POST | Portfolio optimization |

## 🎨 UI Components

Built with **shadcn/ui** components:

- Button, Card, Input, Select, Table
- Dialog, Alert, Badge, Tabs
- Chart, Progress, Skeleton
- And 50+ more components

## 📱 Pages

### 1. Dashboard
- Financial health score gauge
- Monthly expense trends
- Category breakdown
- Quick stats cards

### 2. Expenses
- Add/edit expense form
- Expense table with pagination
- Category filtering
- Delete functionality

### 3. Predictions
- Expense forecast chart
- Personality analysis
- Stress level indicator
- Financial health breakdown

### 4. Investments
- Portfolio allocation chart
- Investment form
- Optimization results
- Performance metrics

## 🔐 Authentication

- JWT token-based authentication
- Automatic token refresh
- Protected routes
- Persistent login state

## 🌐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8080` |
| `VITE_ML_SERVICE_URL` | ML Service URL | `http://localhost:8000` |
| `VITE_APP_NAME` | Application name | `FinGuard AI` |
| `VITE_APP_VERSION` | App version | `1.0.0` |

## 🐛 Troubleshooting

### Port 5173 already in use
```bash
# Kill the process using port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### API connection errors
- Ensure backend is running on port 8080
- Check CORS configuration in backend
- Verify `.env` file has correct API URL

### Build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📜 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Kavindra E M**
- GitHub: [@kavindra-e-m](https://github.com/kavindra-e-m)
- Email: kavindra.em2024aiml@sece.ac.in

## 🙏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for beautiful components
- [Recharts](https://recharts.org/) for data visualization
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Vite](https://vitejs.dev/) for blazing fast builds

---

**FinGuard AI** - Your Intelligent Financial Guardian 🛡️💰
