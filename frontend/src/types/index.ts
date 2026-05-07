export interface User {
  id: number;
  name: string;
  email: string;
  monthlyIncome: number;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
}

export interface Expense {
  id: number;
  category: string;
  amount: number;
  description: string;
  expenseDate: string;
  createdAt: string;
  isAnomaly?: boolean;
}

export interface ExpenseSummary {
  totalThisMonth: number;
  totalLastMonth: number;
  topCategory: string;
  categoryBreakdown: CategoryBreakdown[];
  monthOverMonthChange?: number;
}

export interface CategoryBreakdown {
  category: string;
  amount: number;
  percentage: number;
}

export interface MonthlyTrend {
  month: string;
  total: number;
}

export interface Investment {
  id: number;
  investmentType: string;
  amount: number;
  expectedReturn?: number;
  investmentDate: string;
}

export interface PortfolioOptimization {
  weights: Record<string, number>;
  allocationAmounts: Record<string, number>;
  expectedAnnualReturn: number;
  annualVolatility: number;
  sharpeRatio: number;
  riskLabel: string;
}

export interface ExpensePrediction {
  predictedNextMonth: number;
  confidenceLower: number;
  confidenceUpper: number;
  trend: 'INCREASING' | 'DECREASING' | 'STABLE';
  forecast3Months: number[];
}

export interface PersonalityDetection {
  personalityType: string;
  confidence: number;
  probabilities: Record<string, number>;
  description: string;
}

export interface StressPrediction {
  riskScore: number;
  riskLabel: 'LOW' | 'MEDIUM' | 'HIGH';
  alerts: string[];
  recommendations: string[];
}

export interface FinancialHealth {
  overallScore: number;
  grade: string;
  breakdown: {
    savingsScore: number;
    debtScore: number;
    investmentScore: number;
    expenseStabilityScore: number;
    emergencyFundScore: number;
  };
  recommendations: string[];
  riskFactors: string[];
}

export interface AnomalyDetection {
  anomalies: AnomalyItem[];
  totalAnomalies: number;
  totalTransactions: number;
}

export interface AnomalyItem {
  expenseId: number;
  amount: number;
  category: string;
  anomalyScore: number;
  reason: string;
}
