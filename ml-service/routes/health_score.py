"""
FinGuard AI - Financial Health Score Routes
FastAPI routes for financial health assessment
"""

import logging

from fastapi import APIRouter, HTTPException

from ml.health_scorer import FinancialHealthScorer
from schemas.health_schema import (
    FinancialHealthRequest,
    FinancialHealthResponse,
    GoalTrackerRequest,
    GoalTrackerResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/financial-health-score", response_model=FinancialHealthResponse)
async def calculate_health_score(request: FinancialHealthRequest):
    """
    Calculate comprehensive financial health score.
    
    Returns overall score (0-100), grade, and personalized recommendations.
    """
    try:
        logger.info("Calculating financial health score")
        
        scorer = FinancialHealthScorer()
        result = scorer.calculate_score(
            monthly_income=request.monthly_income,
            monthly_expenses=request.monthly_expenses,
            total_savings=request.total_savings,
            total_debt=request.total_debt,
            monthly_investments=request.monthly_investments,
            emergency_fund=request.emergency_fund,
            expense_trend_3m=request.expense_trend_3m,
            age=request.age
        )
        
        logger.info(f"Health score: {result['overall_score']} ({result['grade']})")
        
        return FinancialHealthResponse(**result)
        
    except Exception as e:
        logger.error(f"Health score calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track-goal", response_model=GoalTrackerResponse)
async def track_financial_goal(request: GoalTrackerRequest):
    """
    Track progress towards a financial goal.
    
    Predicts achievability based on savings rate and expected returns.
    """
    try:
        logger.info(f"Tracking goal: {request.goal_name}")
        
        import numpy as np
        from datetime import datetime
        
        # Calculate months to target
        target_date = datetime.strptime(request.target_date, '%Y-%m-%d')
        today = datetime.now()
        months_to_target = max(1, (target_date.year - today.year) * 12 + 
                              (target_date.month - today.month))
        
        # Calculate progress
        progress = (request.current_saved / request.target_amount * 100) if request.target_amount > 0 else 0
        
        # Project future value with monthly contributions
        monthly_rate = request.expected_return_rate / 12
        future_value = request.current_saved
        
        for month in range(months_to_target):
            future_value = future_value * (1 + monthly_rate) + request.monthly_contribution
        
        # Calculate probability of achievement
        shortfall = request.target_amount - future_value
        if shortfall <= 0:
            probability = 1.0
        else:
            # Simple probability model based on shortfall ratio
            shortfall_ratio = shortfall / request.target_amount
            probability = max(0, 1 - shortfall_ratio * 2)
        
        # Determine if on track
        on_track = future_value >= request.target_amount
        
        # Generate recommendation
        if on_track:
            recommendation = (
                f"You're on track to reach your goal! "
                f"Continue contributing ₹{request.monthly_contribution:,.0f} monthly."
            )
        else:
            additional_needed = (request.target_amount - future_value) / months_to_target
            new_monthly = request.monthly_contribution + additional_needed
            recommendation = (
                f"To reach your goal, consider increasing monthly contribution "
                f"to ₹{new_monthly:,.0f}."
            )
        
        result = {
            'goal_name': request.goal_name,
            'target_amount': request.target_amount,
            'current_saved': request.current_saved,
            'progress_percentage': round(progress, 2),
            'months_to_target': months_to_target,
            'projected_amount': round(future_value, 2),
            'achievement_probability': round(probability, 4),
            'on_track': on_track,
            'recommendation': recommendation
        }
        
        return GoalTrackerResponse(**result)
        
    except Exception as e:
        logger.error(f"Goal tracking failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
