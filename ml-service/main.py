"""
FinGuard AI - ML Service Main Entry Point
FastAPI application for machine learning microservice
"""

import logging
import os
from contextlib import asynccontextmanager

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import anomaly, health_score, personality, portfolio, predict, stress

# Configure logging
log_file = os.path.join(os.path.dirname(__file__), 'logs', 'ml_service.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

# Global model cache
model_cache = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler for startup and shutdown events.
    Loads ML models on startup.
    """
    logger.info("Starting FinGuard AI ML Service...")
    
    # Load models on startup
    models_dir = settings.MODEL_PATH
    if os.path.exists(models_dir):
        model_files = {
            'personality_detector': 'personality_detector.joblib',
            'stress_predictor': 'stress_predictor.joblib',
            'anomaly_detector': 'anomaly_detector.joblib'
        }
        
        for model_name, filename in model_files.items():
            filepath = os.path.join(models_dir, filename)
            if os.path.exists(filepath):
                try:
                    model_cache[model_name] = joblib.load(filepath)
                    logger.info(f"Loaded model: {model_name}")
                except Exception as e:
                    logger.warning(f"Failed to load {model_name}: {str(e)}")
            else:
                logger.warning(f"Model file not found: {filepath}")
    
    logger.info(f"ML Service started. Loaded {len(model_cache)} models.")
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down ML Service...")
    model_cache.clear()


# Create FastAPI application
app = FastAPI(
    title="FinGuard AI - ML Service",
    description="Machine Learning Microservice for Financial Intelligence",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/ml", tags=["Expense Prediction"])
app.include_router(personality.router, prefix="/ml", tags=["Personality Detection"])
app.include_router(stress.router, prefix="/ml", tags=["Stress Prediction"])
app.include_router(portfolio.router, prefix="/ml", tags=["Portfolio Optimization"])
app.include_router(health_score.router, prefix="/ml", tags=["Financial Health Score"])
app.include_router(anomaly.router, prefix="/ml", tags=["Anomaly Detection"])


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "FinGuard AI ML Service",
        "version": "1.0.0",
        "status": "running",
        "loaded_models": list(model_cache.keys())
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring."""
    return {
        "status": "healthy",
        "models_loaded": len(model_cache),
        "service": "ml-service"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
