"""
FinGuard AI - Stress Predictor
Logistic Regression model for financial stress prediction
"""

import logging
from typing import Dict, List, Optional

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)


class StressPredictor:
    """
    Financial stress predictor using Logistic Regression.
    Predicts stress levels: LOW, MEDIUM, or HIGH.
    """
    
    RISK_LABELS = ['LOW', 'MEDIUM', 'HIGH']
    
    def __init__(self, random_state: int = 42):
        """
        Initialize the stress predictor.
        
        Args:
            random_state: Random seed for reproducibility
        """
        self.model = LogisticRegression(
            multi_class='multinomial',
            solver='lbfgs',
            max_iter=1000,
            random_state=random_state,
            class_weight='balanced'
        )
        self.is_trained = False
        self.feature_names = [
            'debt_to_income_ratio',
            'savings_rate',
            'expense_growth_rate',
            'income_stability_score',
            'emergency_fund_months'
        ]
    
    def prepare_features(
        self,
        debt_to_income_ratio: float,
        savings_rate: float,
        expense_growth_rate: float,
        income_stability_score: float,
        emergency_fund_months: float
    ) -> np.ndarray:
        """
        Prepare feature vector for prediction.
        
        Args:
            debt_to_income_ratio: Total debt / monthly income
            savings_rate: Monthly savings / monthly income
            expense_growth_rate: Month-over-month expense growth
            income_stability_score: Income stability (0-1)
            emergency_fund_months: Emergency fund coverage in months
            
        Returns:
            Feature array
        """
        features = np.array([[
            debt_to_income_ratio,
            savings_rate,
            expense_growth_rate,
            income_stability_score,
            emergency_fund_months
        ]])
        return features
    
    def train(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> None:
        """
        Train the stress prediction model.
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target labels (n_samples,) - 0=LOW, 1=MEDIUM, 2=HIGH
        """
        logger.info(f"Training stress predictor on {len(X)} samples")
        
        self.model.fit(X, y)
        self.is_trained = True
        
        # Log coefficients
        if hasattr(self.model, 'coef_'):
            for i, class_label in enumerate(self.RISK_LABELS):
                logger.info(f"Coefficients for {class_label}:")
                for name, coef in zip(self.feature_names, self.model.coef_[i]):
                    logger.info(f"  {name}: {coef:.4f}")
        
        logger.info("Stress predictor trained successfully")
    
    def predict(
        self,
        debt_to_income_ratio: float,
        savings_rate: float,
        expense_growth_rate: float,
        income_stability_score: float,
        emergency_fund_months: float
    ) -> Dict:
        """
        Predict financial stress level.
        
        Args:
            debt_to_income_ratio: Total debt / monthly income
            savings_rate: Monthly savings / monthly income
            expense_growth_rate: Month-over-month expense growth
            income_stability_score: Income stability (0-1)
            emergency_fund_months: Emergency fund coverage in months
            
        Returns:
            Prediction results with alerts and recommendations
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        features = self.prepare_features(
            debt_to_income_ratio, savings_rate, expense_growth_rate,
            income_stability_score, emergency_fund_months
        )
        
        # Get prediction and probabilities
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        risk_label = self.RISK_LABELS[int(prediction)]
        risk_score = float(probabilities[prediction])
        
        # Generate alerts and recommendations
        alerts = self._generate_alerts(
            debt_to_income_ratio, savings_rate, expense_growth_rate,
            emergency_fund_months
        )
        recommendations = self._generate_recommendations(
            debt_to_income_ratio, savings_rate, expense_growth_rate,
            emergency_fund_months, risk_label
        )
        
        return {
            'risk_score': round(risk_score, 4),
            'risk_label': risk_label,
            'alerts': alerts,
            'recommendations': recommendations
        }
    
    def _generate_alerts(
        self,
        debt_to_income_ratio: float,
        savings_rate: float,
        expense_growth_rate: float,
        emergency_fund_months: float
    ) -> List[str]:
        """Generate risk alerts based on financial metrics."""
        alerts = []
        
        if debt_to_income_ratio > 0.40:
            alerts.append(
                f"Debt-to-income ratio is {debt_to_income_ratio:.1%}, "
                "exceeding the recommended 40% threshold."
            )
        
        if savings_rate < 0.15:
            alerts.append(
                f"Savings rate is {savings_rate:.1%}, below the recommended 15%."
            )
        
        if expense_growth_rate > 0.20:
            alerts.append(
                f"Expense growth rate is {expense_growth_rate:.1%}, "
                "exceeding 20% threshold."
            )
        
        if emergency_fund_months < 3:
            alerts.append(
                f"Emergency fund covers only {emergency_fund_months:.1f} months. "
                "Target: 6 months of expenses."
            )
        
        return alerts
    
    def _generate_recommendations(
        self,
        debt_to_income_ratio: float,
        savings_rate: float,
        expense_growth_rate: float,
        emergency_fund_months: float,
        risk_label: str
    ) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        if risk_label == 'HIGH':
            recommendations.append(
                "Priority: Create a strict budget and reduce non-essential spending immediately."
            )
        
        if debt_to_income_ratio > 0.40:
            recommendations.append(
                "Focus on paying down high-interest debt before making new investments."
            )
        
        if savings_rate < 0.15:
            target_savings = 0.20
            increase = (target_savings - savings_rate) * 100
            recommendations.append(
                f"Increase monthly savings by {increase:.0f}% to reach 20% savings rate."
            )
        
        if expense_growth_rate > 0.10:
            recommendations.append(
                "Review recent expenses and identify areas for cost reduction."
            )
        
        if emergency_fund_months < 6:
            target_fund = emergency_fund_months * 1.5  # Rough estimate
            recommendations.append(
                f"Build emergency fund to cover 6 months of expenses."
            )
        
        if risk_label == 'LOW':
            recommendations.append(
                "Your financial health is good. Consider increasing investments for long-term growth."
            )
        
        return recommendations
    
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
        logger.info(f"Stress predictor saved to {filepath}")
    
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
        logger.info(f"Stress predictor loaded from {filepath}")


def predict_stress(
    debt_to_income_ratio: float,
    savings_rate: float,
    expense_growth_rate: float,
    income_stability_score: float,
    emergency_fund_months: float,
    model_path: Optional[str] = None
) -> Dict:
    """
    Convenience function for stress prediction.
    
    Args:
        debt_to_income_ratio: Total debt / monthly income
        savings_rate: Monthly savings / monthly income
        expense_growth_rate: Month-over-month expense growth
        income_stability_score: Income stability (0-1)
        emergency_fund_months: Emergency fund coverage in months
        model_path: Path to trained model (optional)
        
    Returns:
        Stress prediction results
    """
    predictor = StressPredictor()
    
    if model_path:
        predictor.load(model_path)
    else:
        # Use rule-based fallback
        return _rule_based_stress(
            debt_to_income_ratio, savings_rate, expense_growth_rate,
            emergency_fund_months
        )
    
    return predictor.predict(
        debt_to_income_ratio, savings_rate, expense_growth_rate,
        income_stability_score, emergency_fund_months
    )


def _rule_based_stress(
    debt_to_income_ratio: float,
    savings_rate: float,
    expense_growth_rate: float,
    emergency_fund_months: float
) -> Dict:
    """
    Rule-based stress prediction fallback.
    
    Args:
        debt_to_income_ratio: Total debt / monthly income
        savings_rate: Monthly savings / monthly income
        expense_growth_rate: Month-over-month expense growth
        emergency_fund_months: Emergency fund coverage in months
        
    Returns:
        Stress prediction results
    """
    # Calculate risk score
    risk_factors = 0
    
    if debt_to_income_ratio > 0.40:
        risk_factors += 2
    elif debt_to_income_ratio > 0.30:
        risk_factors += 1
    
    if savings_rate < 0.10:
        risk_factors += 2
    elif savings_rate < 0.20:
        risk_factors += 1
    
    if expense_growth_rate > 0.20:
        risk_factors += 2
    elif expense_growth_rate > 0.10:
        risk_factors += 1
    
    if emergency_fund_months < 3:
        risk_factors += 2
    elif emergency_fund_months < 6:
        risk_factors += 1
    
    # Determine risk label
    if risk_factors >= 5:
        risk_label = 'HIGH'
        risk_score = 0.75 + (risk_factors - 5) * 0.05
    elif risk_factors >= 3:
        risk_label = 'MEDIUM'
        risk_score = 0.50 + (risk_factors - 3) * 0.10
    else:
        risk_label = 'LOW'
        risk_score = 0.30 + risk_factors * 0.05
    
    risk_score = min(0.95, risk_score)
    
    predictor = StressPredictor()
    alerts = predictor._generate_alerts(
        debt_to_income_ratio, savings_rate, expense_growth_rate, emergency_fund_months
    )
    recommendations = predictor._generate_recommendations(
        debt_to_income_ratio, savings_rate, expense_growth_rate,
        emergency_fund_months, risk_label
    )
    
    return {
        'risk_score': round(risk_score, 4),
        'risk_label': risk_label,
        'alerts': alerts,
        'recommendations': recommendations
    }
