import { useQuery } from '@tanstack/react-query';
import { TrendingUp, TrendingDown, Wallet, PiggyBank, Brain, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { expenseAPI, analyticsAPI } from '@/services/api';
import type { ExpenseSummary, FinancialHealth, StressPrediction, PersonalityDetection } from '@/types';

export default function DashboardPage() {
  const { data: summary, isLoading: summaryLoading } = useQuery<ExpenseSummary>({
    queryKey: ['expenseSummary'],
    queryFn: async () => {
      const response = await expenseAPI.getSummary();
      return response.data;
    },
  });

  const { data: health, isLoading: healthLoading } = useQuery<FinancialHealth>({
    queryKey: ['financialHealth'],
    queryFn: async () => {
      const response = await analyticsAPI.getFinancialHealth();
      return response.data;
    },
  });

  const { data: stress, isLoading: stressLoading } = useQuery<StressPrediction>({
    queryKey: ['stressPrediction'],
    queryFn: async () => {
      const response = await analyticsAPI.predictStress();
      return response.data;
    },
  });

  const { data: personality, isLoading: personalityLoading } = useQuery<PersonalityDetection>({
    queryKey: ['personality'],
    queryFn: async () => {
      const response = await analyticsAPI.detectPersonality();
      return response.data;
    },
  });

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getHealthColor = (score: number) => {
    if (score >= 80) return 'text-emerald-500';
    if (score >= 60) return 'text-yellow-500';
    if (score >= 40) return 'text-orange-500';
    return 'text-red-500';
  };

  const getStressColor = (label: string) => {
    switch (label) {
      case 'LOW': return 'bg-emerald-100 text-emerald-700';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-700';
      case 'HIGH': return 'bg-red-100 text-red-700';
      default: return 'bg-slate-100 text-slate-700';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-600">Overview of your financial health</p>
      </div>

      {/* Stress Alert */}
      {stress?.riskLabel === 'HIGH' && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            High financial stress detected. Review your expenses and consider reducing discretionary spending.
          </AlertDescription>
        </Alert>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Expenses */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">This Month's Expenses</CardTitle>
            <Wallet className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <>
                <div className="text-2xl font-bold">
                  {formatCurrency(summary?.totalThisMonth || 0)}
                </div>
                {summary?.monthOverMonthChange !== undefined && (
                  <div className={`flex items-center text-sm ${
                    summary.monthOverMonthChange > 0 ? 'text-red-500' : 'text-emerald-500'
                  }`}>
                    {summary.monthOverMonthChange > 0 ? (
                      <TrendingUp className="h-4 w-4 mr-1" />
                    ) : (
                      <TrendingDown className="h-4 w-4 mr-1" />
                    )}
                    {Math.abs(summary.monthOverMonthChange).toFixed(1)}% vs last month
                  </div>
                )}
              </>
            )}
          </CardContent>
        </Card>

        {/* Financial Health Score */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Health Score</CardTitle>
            <PiggyBank className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            {healthLoading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <>
                <div className={`text-2xl font-bold ${getHealthColor(health?.overallScore || 0)}`}>
                  {health?.overallScore || 0}/100
                </div>
                <div className="text-sm text-slate-500">
                  Grade: <span className="font-medium">{health?.grade || 'N/A'}</span>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Personality Badge */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Personality</CardTitle>
            <Brain className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            {personalityLoading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <>
                <div className="text-lg font-bold text-indigo-600">
                  {personality?.personalityType || 'Unknown'}
                </div>
                <div className="text-sm text-slate-500">
                  Confidence: {((personality?.confidence || 0) * 100).toFixed(0)}%
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Stress Level */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Stress Level</CardTitle>
            <AlertTriangle className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            {stressLoading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <>
                <Badge className={getStressColor(stress?.riskLabel || 'LOW')}>
                  {stress?.riskLabel || 'LOW'}
                </Badge>
                <div className="text-sm text-slate-500 mt-1">
                  Risk Score: {((stress?.riskScore || 0) * 100).toFixed(0)}%
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Category Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle>Category Breakdown</CardTitle>
        </CardHeader>
        <CardContent>
          {summaryLoading ? (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-8 w-full" />
              ))}
            </div>
          ) : summary?.categoryBreakdown?.length ? (
            <div className="space-y-4">
              {summary.categoryBreakdown.map((category) => (
                <div key={category.category} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{category.category}</span>
                    <span className="text-slate-600">
                      {formatCurrency(category.amount)} ({category.percentage.toFixed(1)}%)
                    </span>
                  </div>
                  <Progress value={category.percentage} className="h-2" />
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-500 text-center py-4">No expense data available</p>
          )}
        </CardContent>
      </Card>

      {/* Recommendations */}
      {health?.recommendations && health.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>AI Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {health.recommendations.map((rec, index) => (
                <li key={index} className="flex items-start gap-2 text-sm">
                  <span className="text-emerald-500 mt-0.5">•</span>
                  <span className="text-slate-700">{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
