"""
FinGuard AI - Portfolio Optimization Routes
FastAPI routes for investment portfolio optimization
"""

import logging

from fastapi import APIRouter, HTTPException

from ml.portfolio_optimizer import PortfolioOptimizer, get_asset_info
from schemas.portfolio_schema import (
    PortfolioOptimizationRequest,
    PortfolioOptimizationResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/optimize-portfolio", response_model=PortfolioOptimizationResponse)
async def optimize_portfolio(request: PortfolioOptimizationRequest):
    """
    Optimize investment portfolio based on risk tolerance.
    
    Uses Markowitz Modern Portfolio Theory for optimal asset allocation.
    """
    try:
        logger.info(
            f"Optimizing portfolio for {request.risk_tolerance} risk, "
            f"₹{request.available_capital:,.0f} capital"
        )
        
        optimizer = PortfolioOptimizer()
        result = optimizer.optimize(
            risk_tolerance=request.risk_tolerance,
            available_capital=request.available_capital,
            investment_horizon_years=request.investment_horizon_years
        )
        
        logger.info(
            f"Optimization complete: {result['expected_annual_return']:.1%} return, "
            f"{result['sharpe_ratio']:.2f} Sharpe"
        )
        
        return PortfolioOptimizationResponse(**result)
        
    except Exception as e:
        logger.error(f"Portfolio optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/asset-info")
async def get_assets_info():
    """Get information about available asset classes."""
    try:
        return get_asset_info()
    except Exception as e:
        logger.error(f"Failed to get asset info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
