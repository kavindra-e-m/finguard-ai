import { useQuery } from '@tanstack/react-query';
import { TrendingUp, Brain, AlertTriangle, Heart } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Progress } from '@/components/ui/progress';
import { analyticsAPI } from '@/services/api';
import type { ExpensePrediction, PersonalityDetection, StressPrediction, FinancialHealth } from '@/types';

export default function PredictionsPage() {
  const { data: prediction, isLoading: predictionLoading } = useQuery<ExpensePrediction>({
    queryKey: ['expensePrediction'],
    queryFn: async () => {
      const response = await analyticsAPI.predictExpense();
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

  const { data: stress, isLoading: stressLoading } = useQuery<StressPrediction>({
    queryKey: ['stress'],
    queryFn: async () => {
      const response = await analyticsAPI.predictStress();
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

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'INCREASING':
        return <TrendingUp className="h-5 w-5 text-red-500" />;
      case 'DECREASING':
        return <TrendingUp className="h-5 w-5 text-emerald-500 rotate-180" />;
      default:
        return <TrendingUp className="h-5 w-5 text-slate-400" />;
    }
  };

  const getStressColor = (label: string) => {
    switch (label) {
      case 'LOW':
        return 'bg-emerald-100 text-emerald-700 border-emerald-200';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      case 'HIGH':
        return 'bg-red-100 text-red-700 border-red-200';
      default:
        return 'bg-slate-100 text-slate-700';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">AI Predictions</h1>
        <p className="text-slate-600">Machine learning insights for your finances</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Expense Prediction */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-emerald-500" />
              <CardTitle>Expense Forecast</CardTitle>
            </div>
            <CardDescription>Predicted expenses for next month</CardDescription>
          </CardHeader>
          <CardContent>
            {predictionLoading ? (
              <Skeleton className="h-24 w-full" />
            ) : prediction ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500">Predicted Amount</p>
                    <p className="text-3xl font-bold text-slate-900">
                      {formatCurrency(prediction.predictedNextMonth)}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    {getTrendIcon(prediction.trend)}
                    <Badge variant="outline">{prediction.trend}</Badge>
                  </div>
                </div>
                <div className="pt-4 border-t">
                  <p className="text-sm text-slate-500 mb-2">Confidence Interval</p>
                  <div className="flex justify-between text-sm">
                    <span>{formatCurrency(prediction.confidenceLower)}</span>
                    <span>{formatCurrency(prediction.confidenceUpper)}</span>
                  </div>
                  <div className="h-2 bg-slate-100 rounded-full mt-1 relative">
                    <div className="absolute left-1/4 right-1/4 h-full bg-emerald-200 rounded-full" />
                  </div>
                </div>
                <div className="pt-2">
                  <p className="text-sm text-slate-500 mb-2">3-Month Forecast</p>
                  <div className="flex gap-2">
                    {prediction.forecast3Months.map((amount, idx) => (
                      <div key={idx} className="flex-1 bg-slate-50 rounded-lg p-2 text-center">
                        <p className="text-xs text-slate-500">Month {idx + 1}</p>
                        <p className="font-medium">{formatCurrency(amount)}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-slate-500 text-center py-4">No prediction data available</p>
            )}
          </CardContent>
        </Card>

        {/* Personality Detection */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Brain className="h-5 w-5 text-indigo-500" />
              <CardTitle>Financial Personality</CardTitle>
            </div>
            <CardDescription>Your spending behavior profile</CardDescription>
          </CardHeader>
          <CardContent>
            {personalityLoading ? (
              <Skeleton className="h-24 w-full" />
            ) : personality ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500">Detected Type</p>
                    <p className="text-2xl font-bold text-indigo-600">
                      {personality.personalityType}
                    </p>
                  </div>
                  <Badge variant="outline">
                    {((personality.confidence || 0) * 100).toFixed(0)}% confidence
                  </Badge>
                </div>
                <p className="text-slate-600 text-sm">{personality.description}</p>
                <div className="pt-2">
                  <p className="text-sm text-slate-500 mb-2">Probability Distribution</p>
                  <div className="space-y-2">
                    {Object.entries(personality.probabilities || {}).map(([type, prob]) => (
                      <div key={type} className="flex items-center gap-2">
                        <span className="text-xs w-24">{type}</span>
                        <Progress value={(prob as number) * 100} className="h-2 flex-1" />
                        <span className="text-xs w-12 text-right">
                          {((prob as number) * 100).toFixed(0)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-slate-500 text-center py-4">No personality data available</p>
            )}
          </CardContent>
        </Card>

        {/* Stress Prediction */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              <CardTitle>Financial Stress</CardTitle>
            </div>
            <CardDescription>Risk assessment and alerts</CardDescription>
          </CardHeader>
          <CardContent>
            {stressLoading ? (
              <Skeleton className="h-24 w-full" />
            ) : stress ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500">Risk Level</p>
                    <Badge className={getStressColor(stress.riskLabel)}>
                      {stress.riskLabel}
                    </Badge>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-500">Risk Score</p>
                    <p className="text-xl font-bold">
                      {((stress.riskScore || 0) * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>
                {stress.alerts && stress.alerts.length > 0 && (
                  <div className="pt-2">
                    <p className="text-sm text-slate-500 mb-2">Alerts</p>
                    <ul className="space-y-1">
                      {stress.alerts.map((alert, idx) => (
                        <li key={idx} className="text-sm text-red-600 flex items-start gap-2">
                          <AlertTriangle className="h-4 w-4 mt-0.5 flex-shrink-0" />
                          {alert}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {stress.recommendations && stress.recommendations.length > 0 && (
                  <div className="pt-2 border-t">
                    <p className="text-sm text-slate-500 mb-2">Recommendations</p>
                    <ul className="space-y-1">
                      {stress.recommendations.map((rec, idx) => (
                        <li key={idx} className="text-sm text-slate-700 flex items-start gap-2">
                          <span className="text-emerald-500 mt-0.5">•</span>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-slate-500 text-center py-4">No stress data available</p>
            )}
          </CardContent>
        </Card>

        {/* Financial Health Score */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Heart className="h-5 w-5 text-rose-500" />
              <CardTitle>Financial Health</CardTitle>
            </div>
            <CardDescription>Comprehensive health assessment</CardDescription>
          </CardHeader>
          <CardContent>
            {healthLoading ? (
              <Skeleton className="h-24 w-full" />
            ) : health ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500">Overall Score</p>
                    <p className={`text-3xl font-bold ${
                      health.overallScore >= 80 ? 'text-emerald-500' :
                      health.overallScore >= 60 ? 'text-yellow-500' :
                      health.overallScore >= 40 ? 'text-orange-500' : 'text-red-500'
                    }`}>
                      {health.overallScore}/100
                    </p>
                  </div>
                  <Badge variant="outline" className="text-lg">
                    {health.grade}
                  </Badge>
                </div>
                <div className="pt-2">
                  <p className="text-sm text-slate-500 mb-2">Score Breakdown</p>
                  <div className="space-y-2">
                    {Object.entries(health.breakdown || {}).map(([category, score]) => (
                      <div key={category} className="flex items-center gap-2">
                        <span className="text-xs w-32 capitalize">{category.replace(/Score$/, '').replace(/([A-Z])/g, ' $1').trim()}</span>
                        <Progress value={score} className="h-2 flex-1" />
                        <span className="text-xs w-8 text-right">{score}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-slate-500 text-center py-4">No health data available</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
