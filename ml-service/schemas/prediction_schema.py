"""
FinGuard AI - Prediction Schemas
Pydantic models for various prediction endpoints
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PersonalityDetectionRequest(BaseModel):
    """Request schema for financial personality detection."""
    savings_ratio: float = Field(
        ..., 
        description="Savings to income ratio (0-1)", 
        ge=0, 
        le=1,
        example=0.25
    )
    expense_variability: float = Field(
        ..., 
        description="Standard deviation of monthly expenses / mean", 
        ge=0,
        example=0.18
    )
    investment_frequency: int = Field(
        ..., 
        description="Number of investments per month", 
        ge=0,
        example=2
    )
    risk_exposure: float = Field(
        ..., 
        description="High-risk category spend / total spend", 
        ge=0, 
        le=1,
        example=0.30
    )
    food_ratio: float = Field(
        ..., 
        description="Food expenses / total expenses", 
        ge=0, 
        le=1,
        example=0.28
    )
    entertainment_ratio: float = Field(
        ..., 
        description="Entertainment expenses / total expenses", 
        ge=0, 
        le=1,
        example=0.12
    )
    avg_transaction: float = Field(
        ..., 
        description="Average transaction amount", 
        ge=0,
        example=2500.0
    )
    monthly_income: float = Field(
        ..., 
        description="Monthly income amount", 
        ge=0,
        example=50000.0
    )


class PersonalityDetectionResponse(BaseModel):
    """Response schema for personality detection."""
    personality_type: str = Field(
        ..., 
        description="Detected personality type: CONSERVATIVE, BALANCED, AGGRESSIVE, or IMPULSIVE"
    )
    confidence: float = Field(..., description="Confidence score (0-1)", ge=0, le=1)
    probabilities: Dict[str, float] = Field(
        ..., 
        description="Probability scores for each personality type"
    )
    description: str = Field(..., description="Detailed personality description")


class StressPredictionRequest(BaseModel):
    """Request schema for financial stress prediction."""
    debt_to_income_ratio: float = Field(
        ..., 
        description="Total debt / monthly income", 
        ge=0,
        example=0.35
    )
    savings_rate: float = Field(
        ..., 
        description="Monthly savings / monthly income", 
        ge=0, 
        le=1,
        example=0.15
    )
    expense_growth_rate: float = Field(
        ..., 
        description="Month-over-month expense growth rate", 
        example=0.22
    )
    income_stability_score: float = Field(
        ..., 
        description="Income stability score (0-1)", 
        ge=0, 
        le=1,
        example=0.80
    )
    emergency_fund_months: float = Field(
        ..., 
        description="Months of expenses covered by emergency fund", 
        ge=0,
        example=2.0
    )


class StressPredictionResponse(BaseModel):
    """Response schema for stress prediction."""
    risk_score: float = Field(..., description="Risk score (0-1)", ge=0, le=1)
    risk_label: str = Field(..., description="Risk level: LOW, MEDIUM, or HIGH")
    alerts: List[str] = Field(default=[], description="List of risk alerts")
    recommendations: List[str] = Field(default=[], description="List of recommendations")


class RetirementSimulationRequest(BaseModel):
    """Request schema for retirement simulation."""
    current_age: int = Field(..., description="Current age", ge=18, le=100)
    retirement_age: int = Field(..., description="Target retirement age", ge=40, le=100)
    current_savings: float = Field(..., description="Current total savings", ge=0)
    monthly_investment: float = Field(..., description="Monthly investment amount", ge=0)
    expected_return_min: float = Field(
        ..., 
        description="Minimum expected annual return", 
        ge=0, 
        le=1,
        example=0.08
    )
    expected_return_max: float = Field(
        ..., 
        description="Maximum expected annual return", 
        ge=0, 
        le=1,
        example=0.15
    )
    inflation_rate: float = Field(
        default=0.06, 
        description="Annual inflation rate", 
        ge=0, 
        le=1
    )
    target_corpus: Optional[float] = Field(
        None, 
        description="Target retirement corpus (optional)"
    )


class RetirementSimulationResponse(BaseModel):
    """Response schema for retirement simulation."""
    success_probability: float = Field(
        ..., 
        description="Probability of reaching retirement goal (0-1)"
    )
    percentile_10: float = Field(..., description="10th percentile outcome")
    percentile_50: float = Field(..., description="50th percentile (median) outcome")
    percentile_90: float = Field(..., description="90th percentile outcome")
    simulations_run: int = Field(default=1000, description="Number of simulations run")
    years_to_retirement: int = Field(..., description="Years until retirement")
