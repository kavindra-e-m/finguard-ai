"""
FinGuard AI - Personality Detector
Random Forest classifier for financial personality detection
"""

import logging
from typing import Dict, List, Optional

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)


class PersonalityDetector:
    """
    Financial personality detector using Random Forest.
    Classifies users into: CONSERVATIVE, BALANCED, AGGRESSIVE, or IMPULSIVE.
    """
    
    PERSONALITY_TYPES = ['CONSERVATIVE', 'BALANCED', 'AGGRESSIVE', 'IMPULSIVE']
    
    PERSONALITY_DESCRIPTIONS = {
        'CONSERVATIVE': (
            "You are a cautious spender who prioritizes savings and financial security. "
            "You prefer stable investments and avoid unnecessary risks. "
            "Your disciplined approach to money management helps you build "
            "a strong financial foundation."
        ),
        'BALANCED': (
            "You maintain a healthy balance between saving and spending. "
            "You make thoughtful financial decisions while still enjoying life. "
            "Your moderate risk tolerance allows for steady wealth growth "
            "without excessive exposure."
        ),
        'AGGRESSIVE': (
            "You are comfortable with calculated risks and seek higher returns. "
            "You actively pursue investment opportunities and are willing to "
            "accept volatility for potential gains. Your proactive approach "
            "can lead to significant wealth accumulation."
        ),
        'IMPULSIVE': (
            "Your spending patterns show variability with occasional unplanned purchases. "
            "You tend to make spontaneous financial decisions. Consider implementing "
            "a budgeting system to better align your spending with long-term goals."
        )
    }
    
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        """
        Initialize the personality detector.
        
        Args:
            n_estimators: Number of trees in the forest
            random_state: Random seed for reproducibility
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            class_weight='balanced'
        )
        self.is_trained = False
        self.feature_names = [
            'savings_ratio',
            'expense_variability',
            'investment_frequency',
            'risk_exposure',
            'food_ratio',
            'entertainment_ratio',
            'avg_transaction',
            'monthly_income'
        ]
    
    def prepare_features(
        self,
        savings_ratio: float,
        expense_variability: float,
        investment_frequency: int,
        risk_exposure: float,
        food_ratio: float,
        entertainment_ratio: float,
        avg_transaction: float,
        monthly_income: float
    ) -> np.ndarray:
        """
        Prepare feature vector for prediction.
        
        Args:
            savings_ratio: Savings to income ratio
            expense_variability: Expense variability coefficient
            investment_frequency: Number of investments per month
            risk_exposure: High-risk spend ratio
            food_ratio: Food expense ratio
            entertainment_ratio: Entertainment expense ratio
            avg_transaction: Average transaction size
            monthly_income: Monthly income
            
        Returns:
            Feature array
        """
        features = np.array([[
            savings_ratio,
            expense_variability,
            investment_frequency,
            risk_exposure,
            food_ratio,
            entertainment_ratio,
            avg_transaction,
            monthly_income
        ]])
        return features
    
    def train(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> None:
        """
        Train the personality detection model.
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target labels (n_samples,)
        """
        logger.info(f"Training personality detector on {len(X)} samples")
        
        self.model.fit(X, y)
        self.is_trained = True
        
        # Log feature importances
        importances = self.model.feature_importances_
        for name, importance in zip(self.feature_names, importances):
            logger.info(f"  {name}: {importance:.4f}")
        
        logger.info("Personality detector trained successfully")
    
    def predict(
        self,
        savings_ratio: float,
        expense_variability: float,
        investment_frequency: int,
        risk_exposure: float,
        food_ratio: float,
        entertainment_ratio: float,
        avg_transaction: float,
        monthly_income: float
    ) -> Dict:
        """
        Predict financial personality type.
        
        Args:
            savings_ratio: Savings to income ratio
            expense_variability: Expense variability coefficient
            investment_frequency: Number of investments per month
            risk_exposure: High-risk spend ratio
            food_ratio: Food expense ratio
            entertainment_ratio: Entertainment expense ratio
            avg_transaction: Average transaction size
            monthly_income: Monthly income
            
        Returns:
            Prediction results with confidence scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        features = self.prepare_features(
            savings_ratio, expense_variability, investment_frequency,
            risk_exposure, food_ratio, entertainment_ratio,
            avg_transaction, monthly_income
        )
        
        # Get prediction and probabilities
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        # Build probability dictionary
        prob_dict = {
            self.PERSONALITY_TYPES[i]: round(float(prob), 4)
            for i, prob in enumerate(probabilities)
        }
        
        confidence = float(max(probabilities))
        personality_type = self.PERSONALITY_TYPES[int(prediction)]
        
        return {
            'personality_type': personality_type,
            'confidence': round(confidence, 4),
            'probabilities': prob_dict,
            'description': self.PERSONALITY_DESCRIPTIONS[personality_type]
        }
    
    def save(self, filepath: str) -> None:
        """
        Save the trained model.
        
        Args:
            filepath: Path to save the model
        """
        joblib.dump({
            'model': self.model,
            'is_trained': self.is_trained,
            'feature_names': self.feature_names
        }, filepath)
        logger.info(f"Personality detector saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """
        Load trained model.
        
        Args:
            filepath: Path to load the model from
        """
        data = joblib.load(filepath)
        self.model = data['model']
        self.is_trained = data['is_trained']
        self.feature_names = data['feature_names']
        logger.info(f"Personality detector loaded from {filepath}")


def detect_personality(
    savings_ratio: float,
    expense_variability: float,
    investment_frequency: int,
    risk_exposure: float,
    food_ratio: float,
    entertainment_ratio: float,
    avg_transaction: float,
    monthly_income: float,
    model_path: Optional[str] = None
) -> Dict:
    """
    Convenience function for personality detection.
    
    Args:
        savings_ratio: Savings to income ratio
        expense_variability: Expense variability coefficient
        investment_frequency: Number of investments per month
        risk_exposure: High-risk spend ratio
        food_ratio: Food expense ratio
        entertainment_ratio: Entertainment expense ratio
        avg_transaction: Average transaction size
        monthly_income: Monthly income
        model_path: Path to trained model (optional)
        
    Returns:
        Personality detection results
    """
    detector = PersonalityDetector()
    
    if model_path:
        detector.load(model_path)
    else:
        # Use rule-based fallback if no model
        return _rule_based_personality(
            savings_ratio, expense_variability, investment_frequency,
            risk_exposure, food_ratio, entertainment_ratio
        )
    
    return detector.predict(
        savings_ratio, expense_variability, investment_frequency,
        risk_exposure, food_ratio, entertainment_ratio,
        avg_transaction, monthly_income
    )


def _rule_based_personality(
    savings_ratio: float,
    expense_variability: float,
    investment_frequency: int,
    risk_exposure: float,
    food_ratio: float,
    entertainment_ratio: float
) -> Dict:
    """
    Rule-based personality detection fallback.
    
    Args:
        savings_ratio: Savings to income ratio
        expense_variability: Expense variability coefficient
        investment_frequency: Number of investments per month
        risk_exposure: High-risk spend ratio
        food_ratio: Food expense ratio
        entertainment_ratio: Entertainment expense ratio
        
    Returns:
        Personality detection results
    """
    # Simple rule-based classification
    if savings_ratio > 0.3 and risk_exposure < 0.2:
        personality = 'CONSERVATIVE'
        confidence = 0.75
    elif expense_variability > 0.3 or entertainment_ratio > 0.2:
        personality = 'IMPULSIVE'
        confidence = 0.70
    elif investment_frequency >= 2 and risk_exposure > 0.25:
        personality = 'AGGRESSIVE'
        confidence = 0.72
    else:
        personality = 'BALANCED'
        confidence = 0.80
    
    descriptions = PersonalityDetector.PERSONALITY_DESCRIPTIONS
    
    # Generate pseudo-probabilities
    probs = {p: 0.05 for p in ['CONSERVATIVE', 'BALANCED', 'AGGRESSIVE', 'IMPULSIVE']}
    probs[personality] = confidence
    remaining = 1.0 - confidence - 0.15
    for p in probs:
        if p != personality:
            probs[p] = remaining / 3
    
    return {
        'personality_type': personality,
        'confidence': confidence,
        'probabilities': probs,
        'description': descriptions[personality]
    }
