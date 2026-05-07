"""
FinGuard AI - Stress Prediction Routes
FastAPI routes for financial stress prediction
"""

import logging
import os

from fastapi import APIRouter, HTTPException

from ml.stress_predictor import StressPredictor
from schemas.prediction_schema import (
    StressPredictionRequest,
    StressPredictionResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Load model on module import
_predictor = None


def get_predictor():
    """Get or create stress predictor with loaded model."""
    global _predictor
    if _predictor is None:
        model_path = os.getenv(
            'STRESS_MODEL_PATH',
            '/app/models/stress_predictor.joblib'
        )
        
        _predictor = StressPredictor()
        
        if os.path.exists(model_path):
            try:
                _predictor.load(model_path)
                logger.info(f"Loaded stress model from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Using rule-based fallback.")
                _predictor = None
        else:
            logger.warning(f"Model not found at {model_path}. Using rule-based fallback.")
            _predictor = None
    
    return _predictor


@router.post("/predict-stress", response_model=StressPredictionResponse)
async def predict_stress(request: StressPredictionRequest):
    """
    Predict financial stress level based on financial metrics.
    
    Returns risk score and level (LOW, MEDIUM, HIGH) with recommendations.
    """
    try:
        logger.info("Predicting financial stress")
        
        predictor = get_predictor()
        
        if predictor and predictor.is_trained:
            result = predictor.predict(
                debt_to_income_ratio=request.debt_to_income_ratio,
                savings_rate=request.savings_rate,
                expense_growth_rate=request.expense_growth_rate,
                income_stability_score=request.income_stability_score,
                emergency_fund_months=request.emergency_fund_months
            )
        else:
            # Rule-based fallback
            from ml.stress_predictor import _rule_based_stress
            result = _rule_based_stress(
                debt_to_income_ratio=request.debt_to_income_ratio,
                savings_rate=request.savings_rate,
                expense_growth_rate=request.expense_growth_rate,
                emergency_fund_months=request.emergency_fund_months
            )
        
        logger.info(f"Stress level: {result['risk_label']}")
        
        return StressPredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Stress prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
