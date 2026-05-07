"""
FinGuard AI - ML Service Configuration
Environment-based configuration settings
"""

import os
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(extra='allow', env_file='.env', case_sensitive=True)
    
    # Service Configuration
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", os.path.join(os.path.dirname(__file__), "models"))
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://finguard_user:K@VICLOWn17@localhost:5432/finguard_db"
    )
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:8080"
    ).split(",")
    
    # ML Model Parameters
    PERSONALITY_MODEL_PATH: str = os.getenv(
        "PERSONALITY_MODEL_PATH",
        os.path.join(os.path.dirname(__file__), "models", "personality_detector.joblib")
    )
    STRESS_MODEL_PATH: str = os.getenv(
        "STRESS_MODEL_PATH",
        os.path.join(os.path.dirname(__file__), "models", "stress_predictor.joblib")
    )
    ANOMALY_MODEL_PATH: str = os.getenv(
        "ANOMALY_MODEL_PATH",
        os.path.join(os.path.dirname(__file__), "models", "anomaly_detector.joblib")
    )
    
    # Portfolio Optimization Parameters
    RISK_FREE_RATE: float = 0.06  # 6% annual risk-free rate
    
    # Anomaly Detection Parameters
    ANOMALY_CONTAMINATION: float = 0.05  # Expected proportion of anomalies
    
    # Prediction Parameters
    EXPENSE_FORECAST_PERIODS: int = 3  # Number of months to forecast


# Global settings instance
settings = Settings()
