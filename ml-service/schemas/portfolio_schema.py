"""
FinGuard AI - Portfolio Optimization Schemas
Pydantic models for portfolio optimization endpoints
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class PortfolioOptimizationRequest(BaseModel):
    """Request schema for portfolio optimization."""
    risk_tolerance: str = Field(
        ..., 
        description="Risk tolerance level: LOW, MEDIUM, or HIGH"
    )
    available_capital: float = Field(
        ..., 
        description="Available capital for investment", 
        gt=0,
        example=100000
    )
    investment_horizon_years: int = Field(
        default=5, 
        description="Investment horizon in years", 
        ge=1, 
        le=50
    )
    existing_allocations: Optional[Dict[str, float]] = Field(
        default=None, 
        description="Existing portfolio allocations (optional)"
    )
    
    @field_validator('risk_tolerance')
    @classmethod
    def validate_risk_tolerance(cls, v: str) -> str:
        """Validate risk tolerance value."""
        allowed = ['LOW', 'MEDIUM', 'HIGH']
        if v.upper() not in allowed:
            raise ValueError(f"risk_tolerance must be one of {allowed}")
        return v.upper()


class PortfolioOptimizationResponse(BaseModel):
    """Response schema for portfolio optimization."""
    weights: Dict[str, float] = Field(
        ..., 
        description="Optimal allocation weights by asset class"
    )
    allocation_amounts: Dict[str, float] = Field(
        ..., 
        description="Allocation amounts in currency"
    )
    expected_annual_return: float = Field(
        ..., 
        description="Expected annual return (decimal)"
    )
    annual_volatility: float = Field(
        ..., 
        description="Annual volatility/standard deviation (decimal)"
    )
    sharpe_ratio: float = Field(..., description="Sharpe ratio")
    risk_label: str = Field(..., description="Risk classification")


class InvestmentRequest(BaseModel):
    """Request schema for investment creation."""
    investment_type: str = Field(
        ..., 
        description="Type of investment: STOCKS, MUTUAL_FUNDS, BONDS, CRYPTO, GOLD, or FD"
    )
    amount: float = Field(..., description="Investment amount", gt=0)
    expected_return: Optional[float] = Field(
        None, 
        description="Expected annual return percentage"
    )
    investment_date: str = Field(..., description="Investment date in YYYY-MM-DD format")
    
    @field_validator('investment_type')
    @classmethod
    def validate_investment_type(cls, v: str) -> str:
        """Validate investment type."""
        allowed = ['STOCKS', 'MUTUAL_FUNDS', 'BONDS', 'CRYPTO', 'GOLD', 'FD']
        if v.upper() not in allowed:
            raise ValueError(f"investment_type must be one of {allowed}")
        return v.upper()


class InvestmentResponse(BaseModel):
    """Response schema for investment data."""
    id: int = Field(..., description="Investment ID")
    investment_type: str = Field(..., description="Investment type")
    amount: float = Field(..., description="Investment amount")
    expected_return: Optional[float] = Field(None, description="Expected return")
    investment_date: str = Field(..., description="Investment date")
    current_value: Optional[float] = Field(None, description="Current estimated value")


class PortfolioSummaryResponse(BaseModel):
    """Response schema for portfolio summary."""
    total_invested: float = Field(..., description="Total amount invested")
    total_current_value: float = Field(..., description="Current portfolio value")
    total_return: float = Field(..., description="Total return amount")
    return_percentage: float = Field(..., description="Return percentage")
    asset_allocation: Dict[str, float] = Field(..., description="Current allocation by asset")
    investments: List[InvestmentResponse] = Field(..., description="List of investments")
