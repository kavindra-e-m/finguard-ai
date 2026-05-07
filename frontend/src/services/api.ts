import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (name: string, email: string, password: string, monthlyIncome: number) =>
    api.post('/auth/register', { name, email, password, monthlyIncome }),
};

// Expense API
export const expenseAPI = {
  getAll: (page = 0, size = 20) =>
    api.get(`/expenses?page=${page}&size=${size}`),
  create: (data: { category: string; amount: number; description: string; expenseDate: string }) =>
    api.post('/expenses', data),
  delete: (id: number) => api.delete(`/expenses/${id}`),
  getSummary: () => api.get('/expenses/summary'),
  getMonthlyTrend: () => api.get('/expenses/monthly-trend'),
};

// Analytics API
export const analyticsAPI = {
  predictExpense: () => api.get('/analytics/predict-expense'),
  detectPersonality: () => api.get('/analytics/personality'),
  predictStress: () => api.get('/analytics/stress'),
  getFinancialHealth: () => api.get('/analytics/financial-health'),
  detectAnomalies: () => api.get('/analytics/anomalies'),
};

// Investment API
export const investmentAPI = {
  getAll: () => api.get('/investments'),
  create: (data: { investmentType: string; amount: number; expectedReturn?: number; investmentDate: string }) =>
    api.post('/investments', data),
  getSummary: () => api.get('/investments/summary'),
  optimize: (data: { riskTolerance: string; availableCapital: number; investmentHorizonYears?: number }) =>
    api.post('/investments/optimize', data),
};

export default api;
