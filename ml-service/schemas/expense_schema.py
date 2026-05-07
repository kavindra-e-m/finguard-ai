"""
FinGuard AI - Expense Prediction Schemas
Pydantic models for expense prediction endpoints
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class MonthlyExpense(BaseModel):
    """Schema for monthly expense data point."""
    month: str = Field(..., description="Month in YYYY-MM format", example="2024-01")
    amount: float = Field(..., description="Total expense amount for the month", example=15000.0)


class ExpensePredictionRequest(BaseModel):
    """Request schema for expense prediction."""
    user_id: int = Field(..., description="User ID", example=1)
    monthly_expenses: List[MonthlyExpense] = Field(
        ...,
        description="List of monthly expenses (minimum 12 months)",
        min_length=3
    )


class ExpensePredictionResponse(BaseModel):
    """Response schema for expense prediction."""
    predicted_next_month: float = Field(..., description="Predicted expense for next month")
    confidence_lower: float = Field(..., description="Lower bound of confidence interval")
    confidence_upper: float = Field(..., description="Upper bound of confidence interval")
    trend: str = Field(..., description="Trend direction: INCREASING, DECREASING, or STABLE")
    forecast_3_months: List[float] = Field(..., description="3-month forecast values")
    model_used: str = Field(default="prophet", description="ML model used for prediction")


class ExpenseDataPoint(BaseModel):
    """Schema for individual expense transaction."""
    id: int = Field(..., description="Expense ID")
    category: str = Field(..., description="Expense category")
    amount: float = Field(..., description="Expense amount")
    date: str = Field(..., description="Expense date in YYYY-MM-DD format")
    description: Optional[str] = Field(None, description="Optional description")


class AnomalyDetectionRequest(BaseModel):
    """Request schema for anomaly detection."""
    expenses: List[ExpenseDataPoint] = Field(..., description="List of expense transactions")


class AnomalyResult(BaseModel):
    """Schema for detected anomaly."""
    expense_id: int = Field(..., description="ID of anomalous expense")
    amount: float = Field(..., description="Expense amount")
    category: str = Field(..., description="Expense category")
    anomaly_score: float = Field(..., description="Anomaly score (lower is more anomalous)")
    reason: str = Field(..., description="Explanation of why this is anomalous")


class AnomalyDetectionResponse(BaseModel):
    """Response schema for anomaly detection."""
    anomalies: List[AnomalyResult] = Field(default=[], description="List of detected anomalies")
    total_anomalies: int = Field(..., description="Total number of anomalies detected")
    total_transactions: int = Field(..., description="Total transactions analyzed")
