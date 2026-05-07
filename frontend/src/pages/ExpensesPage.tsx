import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Trash2, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
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
import { expenseAPI, analyticsAPI } from '@/services/api';
import type { Expense, AnomalyDetection } from '@/types';

const categories = [
  'FOOD',
  'TRANSPORT',
  'BILLS',
  'ENTERTAINMENT',
  'HEALTHCARE',
  'EDUCATION',
  'SHOPPING',
  'INVESTMENT',
  'SAVINGS',
  'OTHER',
];

export default function ExpensesPage() {
  const queryClient = useQueryClient();
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newExpense, setNewExpense] = useState({
    category: '',
    amount: '',
    description: '',
    expenseDate: new Date().toISOString().split('T')[0],
  });

  const { data: expenses, isLoading } = useQuery<Expense[]>({
    queryKey: ['expenses'],
    queryFn: async () => {
      const response = await expenseAPI.getAll();
      return response.data.content;
    },
  });

  const { data: anomalies } = useQuery<AnomalyDetection>({
    queryKey: ['anomalies'],
    queryFn: async () => {
      const response = await analyticsAPI.detectAnomalies();
      return response.data;
    },
  });

  const anomalyIds = new Set(anomalies?.anomalies.map((a) => a.expenseId) || []);

  const createMutation = useMutation({
    mutationFn: (data: { category: string; amount: number; description: string; expenseDate: string }) =>
      expenseAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      queryClient.invalidateQueries({ queryKey: ['expenseSummary'] });
      setIsDialogOpen(false);
      setNewExpense({
        category: '',
        amount: '',
        description: '',
        expenseDate: new Date().toISOString().split('T')[0],
      });
      toast.success('Expense added successfully');
    },
    onError: () => {
      toast.error('Failed to add expense');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => expenseAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['expenses'] });
      queryClient.invalidateQueries({ queryKey: ['expenseSummary'] });
      toast.success('Expense deleted');
    },
    onError: () => {
      toast.error('Failed to delete expense');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate({
      category: newExpense.category,
      amount: Number(newExpense.amount),
      description: newExpense.description,
      expenseDate: newExpense.expenseDate,
    });
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(amount);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Expenses</h1>
          <p className="text-slate-600">Track and manage your expenses</p>
        </div>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Add Expense
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Add New Expense</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="category">Category</Label>
                <Select
                  value={newExpense.category}
                  onValueChange={(value) => setNewExpense({ ...newExpense, category: value })}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {cat}
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
                  value={newExpense.amount}
                  onChange={(e) => setNewExpense({ ...newExpense, amount: e.target.value })}
                  placeholder="Enter amount"
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Input
                  id="description"
                  value={newExpense.description}
                  onChange={(e) => setNewExpense({ ...newExpense, description: e.target.value })}
                  placeholder="Enter description"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="date">Date</Label>
                <Input
                  id="date"
                  type="date"
                  value={newExpense.expenseDate}
                  onChange={(e) => setNewExpense({ ...newExpense, expenseDate: e.target.value })}
                  required
                />
              </div>
              <Button type="submit" className="w-full" disabled={createMutation.isPending}>
                {createMutation.isPending ? 'Adding...' : 'Add Expense'}
              </Button>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Anomalies Alert */}
      {anomalies && anomalies.totalAnomalies > 0 && (
        <Card className="border-amber-200 bg-amber-50">
          <CardContent className="pt-6">
            <div className="flex items-start gap-3">
              <AlertTriangle className="h-5 w-5 text-amber-600 mt-0.5" />
              <div>
                <p className="font-medium text-amber-900">
                  {anomalies.totalAnomalies} unusual transaction{anomalies.totalAnomalies > 1 ? 's' : ''} detected
                </p>
                <p className="text-sm text-amber-700">
                  Review flagged transactions below for potential errors or fraud.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Recent Expenses</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : expenses?.length ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead className="text-right">Amount</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {expenses.map((expense) => (
                  <TableRow key={expense.id} className={anomalyIds.has(expense.id) ? 'bg-amber-50' : ''}>
                    <TableCell>{expense.expenseDate}</TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        {expense.category}
                        {anomalyIds.has(expense.id) && (
                          <Badge variant="outline" className="border-amber-500 text-amber-700">
                            <AlertTriangle className="h-3 w-3 mr-1" />
                            Unusual
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>{expense.description || '-'}</TableCell>
                    <TableCell className="text-right font-medium">
                      {formatCurrency(expense.amount)}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => deleteMutation.mutate(expense.id)}
                        disabled={deleteMutation.isPending}
                      >
                        <Trash2 className="h-4 w-4 text-red-500" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <p className="text-slate-500 text-center py-8">No expenses recorded yet</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
