"""
FinGuard AI - Master Model Training Script
Trains all ML models for the FinGuard AI platform
"""

import logging
import os
import sys
from typing import Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.seed_data import SeedDataGenerator
from ml.anomaly_detector import AnomalyDetector
from ml.personality_detector import PersonalityDetector
from ml.utils.feature_engineering import FinancialFeatureEngineer
from ml.stress_predictor import StressPredictor
from ml.utils.evaluator import ModelEvaluator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_synthetic_personality_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic training data for personality detection.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Feature matrix and target labels
    """
    np.random.seed(42)
    
    # Generate features for each personality type
    n_per_class = n_samples // 4
    
    # CONSERVATIVE: High savings, low variability, low risk exposure
    conservative = np.array([
        np.random.uniform(0.30, 0.50, n_per_class),  # savings_ratio
        np.random.uniform(0.05, 0.15, n_per_class),  # expense_variability
        np.random.randint(1, 4, n_per_class),        # investment_frequency
        np.random.uniform(0.05, 0.20, n_per_class),  # risk_exposure
        np.random.uniform(0.20, 0.35, n_per_class),  # food_ratio
        np.random.uniform(0.05, 0.12, n_per_class),  # entertainment_ratio
        np.random.uniform(1000, 3000, n_per_class),  # avg_transaction
        np.random.uniform(30000, 80000, n_per_class) # monthly_income
    ]).T
    
    # BALANCED: Moderate values across all features
    balanced = np.array([
        np.random.uniform(0.15, 0.30, n_per_class),
        np.random.uniform(0.10, 0.20, n_per_class),
        np.random.randint(1, 3, n_per_class),
        np.random.uniform(0.15, 0.30, n_per_class),
        np.random.uniform(0.25, 0.35, n_per_class),
        np.random.uniform(0.10, 0.18, n_per_class),
        np.random.uniform(1500, 4000, n_per_class),
        np.random.uniform(30000, 70000, n_per_class)
    ]).T
    
    # AGGRESSIVE: Lower savings, higher investments, higher risk
    aggressive = np.array([
        np.random.uniform(0.10, 0.20, n_per_class),
        np.random.uniform(0.15, 0.25, n_per_class),
        np.random.randint(3, 6, n_per_class),
        np.random.uniform(0.30, 0.50, n_per_class),
        np.random.uniform(0.20, 0.30, n_per_class),
        np.random.uniform(0.15, 0.25, n_per_class),
        np.random.uniform(3000, 8000, n_per_class),
        np.random.uniform(50000, 150000, n_per_class)
    ]).T
    
    # IMPULSIVE: High variability, high entertainment, erratic
    impulsive = np.array([
        np.random.uniform(0.05, 0.20, n_per_class),
        np.random.uniform(0.25, 0.45, n_per_class),
        np.random.randint(0, 2, n_per_class),
        np.random.uniform(0.25, 0.45, n_per_class),
        np.random.uniform(0.25, 0.40, n_per_class),
        np.random.uniform(0.18, 0.35, n_per_class),
        np.random.uniform(2000, 6000, n_per_class),
        np.random.uniform(25000, 60000, n_per_class)
    ]).T
    
    # Combine data
    X = np.vstack([conservative, balanced, aggressive, impulsive])
    y = np.array([0] * n_per_class + [1] * n_per_class + 
                 [2] * n_per_class + [3] * n_per_class)
    
    # Shuffle
    indices = np.random.permutation(len(X))
    return X[indices], y[indices]


def generate_synthetic_stress_data(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic training data for stress prediction.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Feature matrix and target labels
    """
    np.random.seed(43)
    
    n_per_class = n_samples // 3
    
    # LOW stress: Low debt, high savings, stable expenses, good emergency fund
    low_stress = np.array([
        np.random.uniform(0.05, 0.25, n_per_class),  # debt_to_income_ratio
        np.random.uniform(0.20, 0.40, n_per_class),  # savings_rate
        np.random.uniform(-0.10, 0.10, n_per_class), # expense_growth_rate
        np.random.uniform(0.70, 0.95, n_per_class),  # income_stability_score
        np.random.uniform(4.0, 12.0, n_per_class)    # emergency_fund_months
    ]).T
    
    # MEDIUM stress: Moderate values
    medium_stress = np.array([
        np.random.uniform(0.25, 0.40, n_per_class),
        np.random.uniform(0.10, 0.20, n_per_class),
        np.random.uniform(0.05, 0.20, n_per_class),
        np.random.uniform(0.50, 0.75, n_per_class),
        np.random.uniform(2.5, 5.0, n_per_class)
    ]).T
    
    # HIGH stress: High debt, low savings, growing expenses, poor emergency fund
    high_stress = np.array([
        np.random.uniform(0.40, 0.70, n_per_class),
        np.random.uniform(0.00, 0.10, n_per_class),
        np.random.uniform(0.15, 0.35, n_per_class),
        np.random.uniform(0.30, 0.60, n_per_class),
        np.random.uniform(0.0, 2.5, n_per_class)
    ]).T
    
    # Combine data
    X = np.vstack([low_stress, medium_stress, high_stress])
    y = np.array([0] * n_per_class + [1] * n_per_class + [2] * n_per_class)
    
    # Shuffle
    indices = np.random.permutation(len(X))
    return X[indices], y[indices]


def generate_synthetic_anomaly_data(n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic training data for anomaly detection.
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Feature matrix and target labels (1=normal, -1=anomaly)
    """
    np.random.seed(44)
    
    # Normal transactions (95%)
    n_normal = int(n_samples * 0.95)
    normal = np.array([
        np.random.uniform(100, 5000, n_normal),     # amount
        np.random.randint(1, 29, n_normal),         # day_of_month
        np.random.randint(0, 7, n_normal),          # day_of_week
        np.random.randint(1, 13, n_normal),         # month
        np.random.randint(0, 10, n_normal)          # category_encoded
    ]).T
    
    # Anomalous transactions (5%)
    n_anomaly = n_samples - n_normal
    anomaly = np.array([
        np.random.uniform(8000, 50000, n_anomaly),  # very high amount
        np.random.randint(1, 29, n_anomaly),
        np.random.randint(5, 7, n_anomaly),         # weekend
        np.random.randint(1, 13, n_anomaly),
        np.random.randint(0, 10, n_anomaly)
    ]).T
    
    # Combine
    X = np.vstack([normal, anomaly])
    y = np.array([1] * n_normal + [-1] * n_anomaly)
    
    # Shuffle
    indices = np.random.permutation(len(X))
    return X[indices], y[indices]


def extract_personality_features_from_real_data(
    expenses: List[Dict],
    investments: List[Dict],
    monthly_income: float = 50000
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract personality detection features from real data.
    
    Args:
        expenses: List of expense records from database
        investments: List of investment records from database
        monthly_income: Default monthly income for users
        
    Returns:
        Feature matrix and labels (returns matrix even if no labels exist)
    """
    if not expenses:
        logger.warning("No expense data provided")
        return np.array([]).reshape(0, 8), np.array([])
    
    exp_df = pd.DataFrame(expenses)
    exp_df['amount'] = pd.to_numeric(exp_df['amount'], errors='coerce')
    exp_df['expense_date'] = pd.to_datetime(exp_df['expense_date'])
    exp_df = exp_df[exp_df['amount'].notna()]
    
    inv_df = pd.DataFrame(investments) if investments else pd.DataFrame()
    if not inv_df.empty:
        inv_df['amount'] = pd.to_numeric(inv_df['amount'], errors='coerce')
    
    features_list = []
    user_ids = []
    
    for user_id in sorted(exp_df['user_id'].unique()):
        user_expenses = exp_df[exp_df['user_id'] == user_id].copy()
        
        if len(user_expenses) < 10:  # Need minimum transactions
            logger.debug(f"Skipping user {user_id}: insufficient history ({len(user_expenses)} transactions)")
            continue
        
        user_investments = inv_df[inv_df['user_id'] == user_id] if not inv_df.empty else pd.DataFrame()
        
        # Calculate features using FinancialFeatureEngineer
        try:
            monthly_expenses = user_expenses['amount'].sum() / max(1, 
                (user_expenses['expense_date'].max() - user_expenses['expense_date'].min()).days / 30)
            
            user_expenses['category'] = user_expenses['category'].fillna('OTHER')
            
            personality_features = FinancialFeatureEngineer.extract_personality_features(
                monthly_income=monthly_income,
                monthly_expenses=monthly_expenses,
                expenses_df=user_expenses,
                total_savings=monthly_income * 0.2,  # Estimate
                monthly_investments=0 if user_investments.empty else user_investments['amount'].mean()
            )
            
            # Convert dict to array matching model expectations
            feature_vector = [
                personality_features.get('savings_ratio', 0.0),
                personality_features.get('expense_variability', 0.1),
                personality_features.get('investment_frequency', 0),
                personality_features.get('risk_exposure', 0.0),
                personality_features.get('food_ratio', 0.0),
                personality_features.get('entertainment_ratio', 0.0),
                personality_features.get('avg_transaction', 1000),
                personality_features.get('monthly_income', monthly_income)
            ]
            
            features_list.append(feature_vector)
            user_ids.append(user_id)
            
        except Exception as e:
            logger.warning(f"Error extracting features for user {user_id}: {e}")
            continue
    
    if not features_list:
        logger.error("No valid features extracted from real data")
        return np.array([]).reshape(0, 8), np.array([])
    
    logger.info(f"Extracted {len(features_list)} personality feature vectors from {len(user_ids)} unique users")
    return np.array(features_list), np.array(user_ids)


def extract_stress_features_from_real_data(
    expenses: List[Dict],
    investments: List[Dict],
    monthly_income: float = 50000
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract stress prediction features from real data.
    
    Args:
        expenses: List of expense records from database
        investments: List of investment records from database
        monthly_income: Default monthly income for users
        
    Returns:
        Feature matrix and labels (returns matrix even if no labels exist)
    """
    if not expenses:
        logger.warning("No expense data provided")
        return np.array([]).reshape(0, 5), np.array([])
    
    exp_df = pd.DataFrame(expenses)
    exp_df['amount'] = pd.to_numeric(exp_df['amount'], errors='coerce')
    exp_df['expense_date'] = pd.to_datetime(exp_df['expense_date'])
    exp_df = exp_df[exp_df['amount'].notna()]
    
    features_list = []
    user_ids = []
    
    for user_id in sorted(exp_df['user_id'].unique()):
        user_expenses = exp_df[exp_df['user_id'] == user_id].copy()
        
        if len(user_expenses) < 10:
            logger.debug(f"Skipping user {user_id}: insufficient history")
            continue
        
        try:
            user_expenses['category'] = user_expenses['category'].fillna('OTHER')
            monthly_expenses = user_expenses['amount'].sum() / max(1,
                (user_expenses['expense_date'].max() - user_expenses['expense_date'].min()).days / 30)
            
            stress_features = FinancialFeatureEngineer.extract_stress_features(
                monthly_income=monthly_income,
                monthly_expenses=monthly_expenses,
                total_debt=0,  # Not tracked in current schema
                emergency_fund=monthly_income * 3,  # Estimate
                expenses_df=user_expenses
            )
            
            # Convert dict to array matching model expectations
            feature_vector = [
                stress_features.get('debt_to_income_ratio', 0.0),
                stress_features.get('savings_rate', 0.2),
                stress_features.get('expense_growth_rate', 0.0),
                stress_features.get('income_stability_score', 0.75),
                stress_features.get('emergency_fund_months', 3.0)
            ]
            
            features_list.append(feature_vector)
            user_ids.append(user_id)
            
        except Exception as e:
            logger.warning(f"Error extracting stress features for user {user_id}: {e}")
            continue
    
    if not features_list:
        logger.error("No valid stress features extracted from real data")
        return np.array([]).reshape(0, 5), np.array([])
    
    logger.info(f"Extracted {len(features_list)} stress feature vectors from {len(user_ids)} unique users")
    return np.array(features_list), np.array(user_ids)


def extract_anomaly_features_from_real_data(
    expenses: List[Dict]
) -> Tuple[np.ndarray, List[int]]:
    """
    Extract anomaly detection features from real data.
    
    Args:
        expenses: List of expense records from database
        
    Returns:
        Feature matrix and transaction IDs
    """
    if not expenses:
        logger.warning("No expense data provided")
        return np.array([]).reshape(0, 5), []
    
    exp_df = pd.DataFrame(expenses)
    exp_df['amount'] = pd.to_numeric(exp_df['amount'], errors='coerce')
    exp_df['expense_date'] = pd.to_datetime(exp_df['expense_date'])
    exp_df = exp_df[exp_df['amount'].notna()]
    
    category_map = {
        'FOOD': 0, 'TRANSPORT': 1, 'BILLS': 2, 'ENTERTAINMENT': 3,
        'HEALTHCARE': 4, 'EDUCATION': 5, 'SHOPPING': 6, 'INVESTMENT': 7,
        'SAVINGS': 8, 'OTHER': 9
    }
    
    features_list = []
    transaction_ids = []
    
    for _, row in exp_df.iterrows():
        date = row['expense_date']
        
        feature_vector = [
            float(row['amount']),           # amount
            date.day,                       # day_of_month
            date.dayofweek,                 # day_of_week
            date.month,                     # month
            category_map.get(row.get('category', 'OTHER'), 9)  # category_encoded
        ]
        
        features_list.append(feature_vector)
        transaction_ids.append(int(row['id']))
    
    logger.info(f"Extracted {len(features_list)} anomaly feature vectors from {len(exp_df)} transactions")
    return np.array(features_list), transaction_ids


def train_personality_detector(models_dir: str, use_real_data: bool = False, db_url: Optional[str] = None) -> None:
    """
    Train and save personality detection model.
    
    Args:
        models_dir: Directory to save model
        use_real_data: Whether to use real data from database
        db_url: Database URL for real data
    """
    logger.info("=" * 60)
    logger.info("Training Personality Detector")
    if use_real_data:
        logger.info("Using REAL DATA from database")
    else:
        logger.info("Using SYNTHETIC DATA")
    logger.info("=" * 60)
    
    # Generate or load data
    if use_real_data and db_url:
        try:
            expenses, investments = SeedDataGenerator.load_real_data_from_db(db_url)
            X, y = extract_personality_features_from_real_data(expenses, investments)
            
            if len(X) == 0:
                logger.error("No real data extracted. Falling back to synthetic data.")
                X, y = generate_synthetic_personality_data(n_samples=2000)
        except Exception as e:
            logger.error(f"Failed to load real data: {e}. Falling back to synthetic data.")
            X, y = generate_synthetic_personality_data(n_samples=2000)
    else:
        # Use synthetic data
        X, y = generate_synthetic_personality_data(n_samples=2000)
    
    # Split data
    if len(y) > 0 and y.dtype == np.int64:
        # Real labels available (synthetic data)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        # No real labels - split by object type (user IDs from real data)
        unique_users = np.unique(y)
        if len(unique_users) > 1:
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, np.arange(len(X)), test_size=0.2, random_state=42
            )
    
    # Train model
    detector = PersonalityDetector(n_estimators=150, random_state=42)
    detector.train(X_train, y_train)
    
    # Evaluate
    y_pred = detector.model.predict(X_test)
    y_prob = detector.model.predict_proba(X_test)
    
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate_classification(
        y_test, y_pred, y_prob, 
        labels=['CONSERVATIVE', 'BALANCED', 'AGGRESSIVE', 'IMPULSIVE']
    )
    
    evaluator.print_classification_report(metrics)
    
    # Save model
    filepath = os.path.join(models_dir, 'personality_detector.joblib')
    detector.save(filepath)
    
    logger.info(f"Personality detector saved to {filepath}")


def train_stress_predictor(models_dir: str, use_real_data: bool = False, db_url: Optional[str] = None) -> None:
    """
    Train and save stress prediction model.
    
    Args:
        models_dir: Directory to save model
        use_real_data: Whether to use real data from database
        db_url: Database URL for real data
    """
    logger.info("=" * 60)
    logger.info("Training Stress Predictor")
    if use_real_data:
        logger.info("Using REAL DATA from database")
    else:
        logger.info("Using SYNTHETIC DATA")
    logger.info("=" * 60)
    
    # Generate or load data
    if use_real_data and db_url:
        try:
            expenses, investments = SeedDataGenerator.load_real_data_from_db(db_url)
            X, y = extract_stress_features_from_real_data(expenses, investments)
            
            if len(X) == 0:
                logger.error("No real data extracted. Falling back to synthetic data.")
                X, y = generate_synthetic_stress_data(n_samples=1500)
        except Exception as e:
            logger.error(f"Failed to load real data: {e}. Falling back to synthetic data.")
            X, y = generate_synthetic_stress_data(n_samples=1500)
    else:
        # Use synthetic data
        X, y = generate_synthetic_stress_data(n_samples=1500)
    
    # Split data
    if len(y) > 0 and y.dtype == np.int64:
        # Real labels available (synthetic data)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        # No real labels - split by object type (user IDs from real data)
        unique_users = np.unique(y)
        if len(unique_users) > 1:
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, np.arange(len(X)), test_size=0.2, random_state=42
            )
    
    # Train model
    predictor = StressPredictor(random_state=42)
    predictor.train(X_train, y_train)
    
    # Evaluate
    y_pred = predictor.model.predict(X_test)
    y_prob = predictor.model.predict_proba(X_test)
    
    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate_classification(
        y_test, y_pred, y_prob,
        labels=['LOW', 'MEDIUM', 'HIGH']
    )
    
    evaluator.print_classification_report(metrics)
    
    # Save model
    filepath = os.path.join(models_dir, 'stress_predictor.joblib')
    predictor.save(filepath)
    
    logger.info(f"Stress predictor saved to {filepath}")


def train_anomaly_detector(models_dir: str, use_real_data: bool = False, db_url: Optional[str] = None) -> None:
    """
    Train and save anomaly detection model.
    
    Args:
        models_dir: Directory to save model
        use_real_data: Whether to use real data from database
        db_url: Database URL for real data
    """
    logger.info("=" * 60)
    logger.info("Training Anomaly Detector")
    if use_real_data:
        logger.info("Using REAL DATA from database")
    else:
        logger.info("Using SYNTHETIC DATA")
    logger.info("=" * 60)
    
    # Generate or load data
    if use_real_data and db_url:
        try:
            expenses, _ = SeedDataGenerator.load_real_data_from_db(db_url)
            X, _ = extract_anomaly_features_from_real_data(expenses)
            
            if len(X) == 0:
                logger.error("No real data extracted. Falling back to synthetic data.")
                X, y = generate_synthetic_anomaly_data(n_samples=1000)
            else:
                # For real data, we don't have labels, so we'll use unsupervised approach
                y = None
        except Exception as e:
            logger.error(f"Failed to load real data: {e}. Falling back to synthetic data.")
            X, y = generate_synthetic_anomaly_data(n_samples=1000)
    else:
        # Use synthetic data
        X, y = generate_synthetic_anomaly_data(n_samples=1000)
    
    # Split data
    if y is not None:
        # Synthetic data with labels
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        # Real data without labels - use all for training
        X_train = X
        X_test = X[:max(1, len(X) // 5)]
        y_train = None
        y_test = None
    
    # Train model
    detector = AnomalyDetector(contamination=0.05, random_state=42)
    detector.model.fit(X_train)
    detector.is_trained = True
    
    # Evaluate
    if y_test is not None:
        y_pred = detector.model.predict(X_test)
        accuracy = np.mean(y_pred == y_test)
        logger.info(f"Anomaly Detection Accuracy: {accuracy:.4f}")
    else:
        logger.info("Trained on real data without labels. Skipping accuracy evaluation.")
        y_pred = detector.model.predict(X_test)
        anomaly_ratio = np.mean(y_pred == -1)
        logger.info(f"Detected anomaly ratio in test set: {anomaly_ratio:.2%}")
    
    # Save model
    filepath = os.path.join(models_dir, 'anomaly_detector.joblib')
    detector.save(filepath)
    
    logger.info(f"Anomaly detector saved to {filepath}")


def main():
    """Main training function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Train ML models for FinGuard AI")
    parser.add_argument(
        '--use-real-data',
        action='store_true',
        help='Use real data from database instead of synthetic data'
    )
    parser.add_argument(
        '--db-url',
        default=None,
        help='Database URL (e.g., postgresql://user:pass@localhost/finguard_db)'
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("FinGuard AI - Master Model Training")
    logger.info("=" * 60)
    
    # Create models directory
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    logger.info(f"Models will be saved to: {models_dir}")
    
    # Determine database URL
    db_url = args.db_url or os.getenv('DATABASE_URL')
    
    if args.use_real_data and not db_url:
        logger.error("--use-real-data requires --db-url or DATABASE_URL environment variable")
        logger.info("Falling back to synthetic data...")
        args.use_real_data = False
    
    try:
        # Train all models
        train_personality_detector(models_dir, args.use_real_data, db_url)
        train_stress_predictor(models_dir, args.use_real_data, db_url)
        train_anomaly_detector(models_dir, args.use_real_data, db_url)
        
        logger.info("=" * 60)
        logger.info("All models trained successfully!")
        logger.info("=" * 60)
        
        # List saved models
        models = os.listdir(models_dir)
        logger.info("Saved models:")
        for model in models:
            filepath = os.path.join(models_dir, model)
            size = os.path.getsize(filepath)
            logger.info(f"  {model}: {size / 1024:.1f} KB")
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise


if __name__ == "__main__":
    main()
