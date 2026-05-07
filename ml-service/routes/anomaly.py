"""
FinGuard AI - Anomaly Detection Routes
FastAPI routes for expense anomaly detection
"""

import logging
import os

from fastapi import APIRouter, HTTPException

from ml.anomaly_detector import AnomalyDetector
from schemas.expense_schema import (
    AnomalyDetectionRequest,
    AnomalyDetectionResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()

# Load model on module import
_detector = None


def get_detector():
    """Get or create anomaly detector with loaded model."""
    global _detector
    if _detector is None:
        model_path = os.getenv(
            'ANOMALY_MODEL_PATH',
            '/app/models/anomaly_detector.joblib'
        )
        
        _detector = AnomalyDetector()
        
        if os.path.exists(model_path):
            try:
                _detector.load(model_path)
                logger.info(f"Loaded anomaly model from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Using rule-based fallback.")
                _detector = None
        else:
            logger.warning(f"Model not found at {model_path}. Using rule-based fallback.")
            _detector = None
    
    return _detector


@router.post("/detect-anomalies", response_model=AnomalyDetectionResponse)
async def detect_anomalies(request: AnomalyDetectionRequest):
    """
    Detect anomalous expense transactions.
    
    Uses Isolation Forest to identify unusual spending patterns.
    """
    try:
        logger.info(f"Detecting anomalies in {len(request.expenses)} transactions")
        
        if not request.expenses:
            return AnomalyDetectionResponse(
                anomalies=[],
                total_anomalies=0,
                total_transactions=0
            )
        
        detector = get_detector()
        
        # Convert to list of dicts
        expenses_data = [
            {
                'id': exp.id,
                'category': exp.category,
                'amount': exp.amount,
                'date': exp.date
            }
            for exp in request.expenses
        ]
        
        if detector and detector.is_trained:
            result = detector.detect(expenses_data)
        else:
            # Rule-based fallback
            from ml.anomaly_detector import detect_simple_anomalies
            result = detect_simple_anomalies(expenses_data)
        
        logger.info(f"Detected {result['total_anomalies']} anomalies")
        
        return AnomalyDetectionResponse(**result)
        
    except Exception as e:
        logger.error(f"Anomaly detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
