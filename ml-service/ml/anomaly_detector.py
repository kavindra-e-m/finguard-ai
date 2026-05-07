"""
FinGuard AI - Anomaly Detector
Isolation Forest for detecting unusual expense transactions
"""

import logging
from typing import Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Anomaly detection for expense transactions using Isolation Forest.
    Identifies unusual spending patterns and outliers.
    """
    
    def __init__(
        self, 
        contamination: float = 0.05,
        random_state: int = 42
    ):
        """
        Initialize the anomaly detector.
        
        Args:
            contamination: Expected proportion of anomalies in data
            random_state: Random seed for reproducibility
        """
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=random_state,
            max_samples='auto',
            max_features=1.0
        )
        self.is_trained = False
        self.contamination = contamination
        
        # Category encoding
        self.category_mapping = {}
        self.category_stats = {}
    
    def prepare_features(
        self, 
        expenses: List[Dict]
    ) -> pd.DataFrame:
        """
        Prepare features for anomaly detection.
        
        Args:
            expenses: List of expense transactions
            
        Returns:
            Feature DataFrame
        """
        df = pd.DataFrame(expenses)
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract time features
        df['day_of_month'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        
        # Encode category
        if not self.category_mapping:
            categories = df['category'].unique()
            self.category_mapping = {cat: i for i, cat in enumerate(categories)}
        
        df['category_encoded'] = df['category'].map(self.category_mapping)
        
        # Calculate category statistics for context
        self._calculate_category_stats(df)
        
        # Create features
        features = pd.DataFrame({
            'amount': df['amount'],
            'day_of_month': df['day_of_month'],
            'day_of_week': df['day_of_week'],
            'month': df['month'],
            'category_encoded': df['category_encoded']
        })
        
        return features
    
    def _calculate_category_stats(self, df: pd.DataFrame) -> None:
        """Calculate statistics for each category."""
        for category in df['category'].unique():
            cat_data = df[df['category'] == category]['amount']
            self.category_stats[category] = {
                'mean': cat_data.mean(),
                'std': cat_data.std(),
                'median': cat_data.median(),
                'max': cat_data.max(),
                'min': cat_data.min()
            }
    
    def train(self, expenses: List[Dict]) -> None:
        """
        Train the anomaly detection model.
        
        Args:
            expenses: List of expense transactions
        """
        if len(expenses) < 10:
            logger.warning("Insufficient data for anomaly detection training")
            return
        
        logger.info(f"Training anomaly detector on {len(expenses)} transactions")
        
        features = self.prepare_features(expenses)
        self.model.fit(features)
        self.is_trained = True
        
        logger.info("Anomaly detector trained successfully")
    
    def detect(
        self, 
        expenses: List[Dict]
    ) -> Dict:
        """
        Detect anomalies in expense transactions.
        
        Args:
            expenses: List of expense transactions
            
        Returns:
            Detection results with anomaly details
        """
        if not expenses:
            return {
                'anomalies': [],
                'total_anomalies': 0,
                'total_transactions': 0
            }
        
        if not self.is_trained:
            # Train on current data if not already trained
            self.train(expenses)
        
        features = self.prepare_features(expenses)
        
        # Get anomaly predictions and scores
        predictions = self.model.predict(features)
        scores = self.model.decision_function(features)
        
        # Build results
        anomalies = []
        for i, (expense, pred, score) in enumerate(zip(expenses, predictions, scores)):
            if pred == -1:  # Anomaly
                reason = self._generate_anomaly_reason(expense)
                anomalies.append({
                    'expense_id': expense.get('id', i),
                    'amount': expense['amount'],
                    'category': expense['category'],
                    'anomaly_score': round(float(score), 4),
                    'reason': reason
                })
        
        return {
            'anomalies': anomalies,
            'total_anomalies': len(anomalies),
            'total_transactions': len(expenses)
        }
    
    def _generate_anomaly_reason(self, expense: Dict) -> str:
        """Generate explanation for why a transaction is anomalous."""
        category = expense['category']
        amount = expense['amount']
        
        if category in self.category_stats:
            stats = self.category_stats[category]
            mean = stats['mean']
            std = stats['std'] if stats['std'] > 0 else mean * 0.1
            
            z_score = (amount - mean) / std
            
            if z_score > 3:
                return (
                    f"Amount is {z_score:.1f} standard deviations above your "
                    f"average {category.lower()} spend."
                )
            elif z_score > 2:
                ratio = amount / mean if mean > 0 else 0
                return (
                    f"Amount is {ratio:.1f}x your average {category.lower()} spend."
                )
        
        # Check for unusual timing
        date = pd.to_datetime(expense.get('date', ''))
        if date.dayofweek in [5, 6]:  # Weekend
            return "Unusually large weekend transaction."
        
        return "Transaction pattern differs significantly from your normal spending."
    
    def save(self, filepath: str) -> None:
        """
        Save the trained model.
        
        Args:
            filepath: Path to save the model
        """
        joblib.dump({
            'model': self.model,
            'is_trained': self.is_trained,
            'category_mapping': self.category_mapping,
            'category_stats': self.category_stats,
            'contamination': self.contamination
        }, filepath)
        logger.info(f"Anomaly detector saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """
        Load trained model.
        
        Args:
            filepath: Path to load the model from
        """
        data = joblib.load(filepath)
        self.model = data['model']
        self.is_trained = data['is_trained']
        self.category_mapping = data['category_mapping']
        self.category_stats = data['category_stats']
        self.contamination = data['contamination']
        logger.info(f"Anomaly detector loaded from {filepath}")


def detect_anomalies(
    expenses: List[Dict],
    model_path: Optional[str] = None
) -> Dict:
    """
    Convenience function for anomaly detection.
    
    Args:
        expenses: List of expense transactions
        model_path: Path to trained model (optional)
        
    Returns:
        Anomaly detection results
    """
    detector = AnomalyDetector()
    
    if model_path:
        detector.load(model_path)
    
    return detector.detect(expenses)


def detect_simple_anomalies(expenses: List[Dict]) -> Dict:
    """
    Simple rule-based anomaly detection without ML.
    
    Args:
        expenses: List of expense transactions
        
    Returns:
        Anomaly detection results
    """
    if not expenses:
        return {
            'anomalies': [],
            'total_anomalies': 0,
            'total_transactions': 0
        }
    
    # Calculate category statistics
    df = pd.DataFrame(expenses)
    category_stats = {}
    
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]['amount']
        category_stats[category] = {
            'mean': cat_data.mean(),
            'std': cat_data.std()
        }
    
    # Detect anomalies
    anomalies = []
    for i, expense in enumerate(expenses):
        category = expense['category']
        amount = expense['amount']
        
        if category in category_stats:
            stats = category_stats[category]
            mean = stats['mean']
            std = stats['std'] if stats['std'] > 0 else mean * 0.1
            
            z_score = abs((amount - mean) / std) if std > 0 else 0
            
            if z_score > 2.5:  # More than 2.5 standard deviations
                ratio = amount / mean if mean > 0 else 0
                anomalies.append({
                    'expense_id': expense.get('id', i),
                    'amount': amount,
                    'category': category,
                    'anomaly_score': round(-z_score / 10, 4),
                    'reason': (
                        f"Amount is {ratio:.1f}x your average {category.lower()} spend."
                    )
                })
    
    return {
        'anomalies': anomalies,
        'total_anomalies': len(anomalies),
        'total_transactions': len(expenses)
    }
