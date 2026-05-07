"""
FinGuard AI - Personality Detection Routes
FastAPI routes for financial personality detection
"""

import logging
import os

from fastapi import APIRouter, HTTPException

from ml.personality_detector import PersonalityDetector
from schemas.prediction_schema import (
    PersonalityDetectionRequest,
    PersonalityDetectionResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Load model on module import
_detector = None


def get_detector():
    """Get or create personality detector with loaded model."""
    global _detector
    if _detector is None:
        model_path = os.getenv(
            'PERSONALITY_MODEL_PATH',
            '/app/models/personality_detector.joblib'
        )
        
        _detector = PersonalityDetector()
        
        if os.path.exists(model_path):
            try:
                _detector.load(model_path)
                logger.info(f"Loaded personality model from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Using rule-based fallback.")
                _detector = None
        else:
            logger.warning(f"Model not found at {model_path}. Using rule-based fallback.")
            _detector = None
    
    return _detector


@router.post("/detect-personality", response_model=PersonalityDetectionResponse)
async def detect_personality(request: PersonalityDetectionRequest):
    """
    Detect financial personality type based on spending behavior.
    
    Returns one of: CONSERVATIVE, BALANCED, AGGRESSIVE, IMPULSIVE
    """
    try:
        logger.info("Detecting financial personality")
        
        detector = get_detector()
        
        if detector and detector.is_trained:
            result = detector.predict(
                savings_ratio=request.savings_ratio,
                expense_variability=request.expense_variability,
                investment_frequency=request.investment_frequency,
                risk_exposure=request.risk_exposure,
                food_ratio=request.food_ratio,
                entertainment_ratio=request.entertainment_ratio,
                avg_transaction=request.avg_transaction,
                monthly_income=request.monthly_income
            )
        else:
            # Rule-based fallback
            from ml.personality_detector import _rule_based_personality
            result = _rule_based_personality(
                savings_ratio=request.savings_ratio,
                expense_variability=request.expense_variability,
                investment_frequency=request.investment_frequency,
                risk_exposure=request.risk_exposure,
                food_ratio=request.food_ratio,
                entertainment_ratio=request.entertainment_ratio
            )
        
        logger.info(f"Personality detected: {result['personality_type']}")
        
        return PersonalityDetectionResponse(**result)
        
    except Exception as e:
        logger.error(f"Personality detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
