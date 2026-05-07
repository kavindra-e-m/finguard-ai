"""
FinGuard AI - Expense Prediction Routes
FastAPI routes for expense forecasting
"""

import logging
from typing import List

from fastapi import APIRouter, HTTPException

from ml.expense_predictor import ExpensePredictor
from schemas.expense_schema import (
    ExpensePredictionRequest,
    ExpensePredictionResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/predict-expense", response_model=ExpensePredictionResponse)
async def predict_expense(request: ExpensePredictionRequest):
    """
    Predict future expenses based on historical data.
    
    Uses Prophet time series forecasting with Linear Regression fallback.
    """
    try:
        logger.info(f"Predicting expenses for user {request.user_id}")
        
        # Validate data
        if len(request.monthly_expenses) < 3:
            raise HTTPException(
                status_code=400,
                detail="At least 3 months of data required for prediction"
            )
        
        # Convert to format expected by predictor
        monthly_data = [
            {"month": exp.month, "amount": exp.amount}
            for exp in request.monthly_expenses
        ]
        
        # Create predictor and make prediction
        predictor = ExpensePredictor()
        predictor.train(monthly_data)
        result = predictor.predict(periods=3)
        
        logger.info(f"Prediction complete: {result['predicted_next_month']}")
        
        return ExpensePredictionResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
