import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, TrendingUp, PieChart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';
import { investmentAPI } from '@/services/api';
import type { Investment, PortfolioOptimization } from '@/types';

const investmentTypes = ['STOCKS', 'MUTUAL_FUNDS', 'BONDS', 'CRYPTO', 'GOLD', 'FD'];

export default function InvestmentsPage() {
  const queryClient = useQueryClient();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [showOptimizer, setShowOptimizer] = useState(false);
  const [newInvestment, setNewInvestment] = useState({
    investmentType: '',
    amount: '',
    expectedReturn: '',
    investmentDate: new Date().toISOString().split('T')[0],
  });
  const [optimizerParams, setOptimizerParams] = useState({
    riskTolerance: 'MEDIUM',
    availableCapital: 100000,
    investmentHorizonYears: 5,
  });

  const { data: investments, isLoading } = useQuery<Investment[]>({
    queryKey: ['investments'],
    queryFn: async () => {
      const response = await investmentAPI.getAll();
      return response.data;
    },
  });

  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ['portfolioSummary'],
    queryFn: async () => {
      const response = await investmentAPI.getSummary();
      return response.data;
    },
  });

  const { data: optimization, refetch: refetchOptimization } = useQuery<PortfolioOptimization>({
    queryKey: ['portfolioOptimization'],
    queryFn: async () => {
      const response = await investmentAPI.optimize({
        riskTolerance: optimizerParams.riskTolerance,
        availableCapital: optimizerParams.availableCapital,
        investmentHorizonYears: optimizerParams.investmentHorizonYears,
      });
      return response.data;
    },
    enabled: false,
  });

  const createMutation = useMutation({
    mutationFn: (data: { investmentType: string; amount: number; expectedReturn?: number; investmentDate: string }) =>
      investmentAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['investments'] });
      queryClient.invalidateQueries({ queryKey: ['portfolioSummary'] });
      setIsDialogOpen(false);
      setNewInvestment({
        investmentType: '',
        amount: '',
        expectedReturn: '',
        investmentDate: new Date().toISOString().split('T')[0],
      });
      toast.success('Investment added successfully');
    },
    onError: () => {
      toast.error('Failed to add investment');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate({
      investmentType: newInvestment.investmentType,
      amount: Number(newInvestment.amount),
      expectedReturn: newInvestment.expectedReturn ? Number(newInvestment.expectedReturn) : undefined,
      investmentDate: newInvestment.investmentDate,
    });
  };

  const handleOptimize = () => {
    refetchOptimization();
    setShowOptimizer(true);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(2)}%`;
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Investments</h1>
          <p className="text-slate-600">Manage your investment portfolio</p>
        </div>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Investment
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Investment</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="type">Investment Type</Label>
                <Select
                  value={newInvestment.investmentType}
                  onValueChange={(value) => setNewInvestment({ ...newInvestment, investmentType: value })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    {investmentTypes.map((type) => (
                      <SelectItem key={type} value={type}>
                        {type.replace('_', ' ')}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="amount">Amount (₹)</Label>
                <Input
                  id="amount"
                  type="number"
                  value={newInvestment.amount}
                  onChange={(e) => setNewInvestment({ ...newInvestment, amount: e.target.value })}
                  placeholder="Enter amount"
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="expectedReturn">Expected Return (%)</Label>
                <Input
                  id="expectedReturn"
                  type="number"
                  step="0.01"
                  value={newInvestment.expectedReturn}
                  onChange={(e) => setNewInvestment({ ...newInvestment, expectedReturn: e.target.value })}
                  placeholder="e.g., 12"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="date">Investment Date</Label>
                <Input
                  id="date"
                  type="date"
                  value={newInvestment.investmentDate}
                  onChange={(e) => setNewInvestment({ ...newInvestment, investmentDate: e.target.value })}
                  required
                />
              </div>
              <Button type="submit" className="w-full" disabled={createMutation.isPending}>
                {createMutation.isPending ? 'Adding...' : 'Add Investment'}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Total Invested</CardTitle>
            <PieChart className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <div className="text-2xl font-bold">
                {formatCurrency(summary?.totalInvested || 0)}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Current Value</CardTitle>
            <TrendingUp className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <div className="text-2xl font-bold">
                {formatCurrency(summary?.totalCurrentValue || 0)}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-600">Total Return</CardTitle>
            <TrendingUp className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            {summaryLoading ? (
              <Skeleton className="h-8 w-32" />
            ) : (
              <div className={`text-2xl font-bold ${
                (summary?.returnPercentage || 0) >= 0 ? 'text-emerald-500' : 'text-red-500'
              }`}>
                {(summary?.returnPercentage || 0) >= 0 ? '+' : ''}
                {(summary?.returnPercentage || 0).toFixed(2)}%
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Portfolio Optimizer */}
      <Card>
        <CardHeader>
          <CardTitle>Portfolio Optimizer</CardTitle>
          <CardDescription>Get AI-recommended asset allocation</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <Label>Risk Tolerance</Label>
              <Select
                value={optimizerParams.riskTolerance}
                onValueChange={(value) => setOptimizerParams({ ...optimizerParams, riskTolerance: value })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="LOW">Low Risk</SelectItem>
                  <SelectItem value="MEDIUM">Medium Risk</SelectItem>
                  <SelectItem value="HIGH">High Risk</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Available Capital (₹)</Label>
              <Input
                type="number"
                value={optimizerParams.availableCapital}
                onChange={(e) => setOptimizerParams({ ...optimizerParams, availableCapital: Number(e.target.value) })}
              />
            </div>
            <div className="flex items-end">
              <Button onClick={handleOptimize} className="w-full">
                Optimize Portfolio
              </Button>
            </div>
          </div>

          {showOptimizer && optimization && (
            <div className="border rounded-lg p-4 space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm text-slate-500">Expected Annual Return</p>
                  <p className="text-xl font-bold text-emerald-600">
                    {formatPercentage(optimization.expectedAnnualReturn)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Annual Volatility</p>
                  <p className="text-xl font-bold text-slate-700">
                    {formatPercentage(optimization.annualVolatility)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Sharpe Ratio</p>
                  <p className="text-xl font-bold text-indigo-600">
                    {optimization.sharpeRatio.toFixed(2)}
                  </p>
                </div>
                <Badge variant="outline">{optimization.riskLabel} Risk</Badge>
              </div>

              <div className="pt-4 border-t">
                <p className="text-sm font-medium mb-3">Recommended Allocation</p>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {Object.entries(optimization.weights).map(([asset, weight]) => (
                    <div key={asset} className="bg-slate-50 rounded-lg p-3">
                      <p className="text-xs text-slate-500">{asset.replace('_', ' ')}</p>
                      <p className="font-medium">{(weight * 100).toFixed(1)}%</p>
                      <p className="text-xs text-slate-600">
                        {formatCurrency(optimization.allocationAmounts[asset])}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Investments Table */}
      <Card>
        <CardHeader>
          <CardTitle>Your Investments</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : investments?.length ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Type</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead className="text-right">Amount</TableHead>
                  <TableHead className="text-right">Expected Return</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {investments.map((investment) => (
                  <TableRow key={investment.id}>
                    <TableCell>
                      <Badge variant="outline">
                        {investment.investmentType.replace('_', ' ')}
                      </Badge>
                    </TableCell>
                    <TableCell>{investment.investmentDate}</TableCell>
                    <TableCell className="text-right font-medium">
                      {formatCurrency(investment.amount)}
                    </TableCell>
                    <TableCell className="text-right">
                      {investment.expectedReturn
                        ? `${(investment.expectedReturn * 100).toFixed(2)}%`
                        : '-'}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <p className="text-slate-500 text-center py-8">No investments recorded yet</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
