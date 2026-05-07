"""
FinGuard AI - Financial Health Score Schemas
Pydantic models for financial health assessment endpoints
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class FinancialHealthRequest(BaseModel):
    """Request schema for financial health score calculation."""
    monthly_income: float = Field(
        ..., 
        description="Monthly income amount", 
        ge=0,
        example=50000
    )
    monthly_expenses: float = Field(
        ..., 
        description="Monthly expense amount", 
        ge=0,
        example=32000
    )
    total_savings: float = Field(
        ..., 
        description="Total savings amount", 
        ge=0,
        example=120000
    )
    total_debt: float = Field(
        ..., 
        description="Total debt amount", 
        ge=0,
        example=80000
    )
    monthly_investments: float = Field(
        ..., 
        description="Monthly investment amount", 
        ge=0,
        example=5000
    )
    emergency_fund: float = Field(
        ..., 
        description="Emergency fund amount", 
        ge=0,
        example=90000
    )
    expense_trend_3m: List[float] = Field(
        ..., 
        description="Expense trend for last 3 months",
        min_length=3,
        max_length=3,
        example=[30000, 31000, 32000]
    )
    age: Optional[int] = Field(
        None, 
        description="User age (optional)", 
        ge=18, 
        le=100
    )


class FinancialHealthResponse(BaseModel):
    """Response schema for financial health score."""
    overall_score: int = Field(
        ..., 
        description="Overall financial health score (0-100)", 
        ge=0, 
        le=100
    )
    grade: str = Field(
        ..., 
        description="Letter grade: EXCELLENT, GOOD, FAIR, or POOR"
    )
    breakdown: Dict[str, int] = Field(
        ..., 
        description="Score breakdown by category"
    )
    recommendations: List[str] = Field(
        default=[], 
        description="Personalized recommendations"
    )
    risk_factors: List[str] = Field(
        default=[], 
        description="Identified risk factors"
    )


class GoalTrackerRequest(BaseModel):
    """Request schema for financial goal tracking."""
    goal_name: str = Field(..., description="Name of the financial goal")
    target_amount: float = Field(..., description="Target amount to achieve", gt=0)
    target_date: str = Field(..., description="Target date in YYYY-MM-DD format")
    current_saved: float = Field(..., description="Amount already saved", ge=0)
    monthly_contribution: float = Field(
        ..., 
        description="Monthly contribution amount", 
        ge=0
    )
    expected_return_rate: float = Field(
        default=0.08, 
        description="Expected annual return rate", 
        ge=0, 
        le=1
    )


class GoalTrackerResponse(BaseModel):
    """Response schema for goal tracking."""
    goal_name: str = Field(..., description="Goal name")
    target_amount: float = Field(..., description="Target amount")
    current_saved: float = Field(..., description="Current saved amount")
    progress_percentage: float = Field(
        ..., 
        description="Progress towards goal (0-100)"
    )
    months_to_target: int = Field(..., description="Months until target date")
    projected_amount: float = Field(
        ..., 
        description="Projected amount at target date"
    )
    achievement_probability: float = Field(
        ..., 
        description="Probability of achieving goal (0-1)"
    )
    on_track: bool = Field(..., description="Whether goal is on track")
    recommendation: str = Field(
        ..., 
        description="Recommendation for achieving goal"
    )


class EmotionalSpendingRequest(BaseModel):
    """Request schema for emotional spending analysis."""
    expenses: List[Dict] = Field(
        ..., 
        description="List of expense transactions with date, time, category, amount"
    )
    salary_credit_day: Optional[int] = Field(
        None, 
        description="Day of month when salary is credited", 
        ge=1, 
        le=31
    )


class EmotionalSpendingResponse(BaseModel):
    """Response schema for emotional spending analysis."""
    has_emotional_spending_pattern: bool = Field(
        ..., 
        description="Whether emotional spending patterns detected"
    )
    patterns: List[Dict] = Field(
        default=[], 
        description="Detected spending patterns"
    )
    weekend_spending_ratio: float = Field(
        ..., 
        description="Weekend spending vs weekday ratio"
    )
    post_salary_spike: Optional[float] = Field(
        None, 
        description="Spending spike after salary credit"
    )
    insights: List[str] = Field(..., description="Behavioral insights")
    recommendations: List[str] = Field(..., description="Recommendations")
