"""
FinGuard AI - Model Evaluator
Utilities for evaluating ML model performance
"""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluator for machine learning models."""
    
    @staticmethod
    def evaluate_classification(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None,
        labels: Optional[List[str]] = None
    ) -> Dict:
        """
        Evaluate classification model performance.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Predicted probabilities (optional)
            labels: Class labels (optional)
            
        Returns:
            Dictionary of evaluation metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision_macro': precision_score(y_true, y_pred, average='macro', zero_division=0),
            'recall_macro': recall_score(y_true, y_pred, average='macro', zero_division=0),
            'f1_macro': f1_score(y_true, y_pred, average='macro', zero_division=0),
            'precision_weighted': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall_weighted': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1_weighted': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        }
        
        # Add per-class metrics
        class_report = classification_report(
            y_true, y_pred, 
            target_names=labels,
            output_dict=True,
            zero_division=0
        )
        metrics['per_class'] = class_report
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        # ROC AUC (for binary or if probabilities provided)
        if y_prob is not None:
            try:
                if len(np.unique(y_true)) == 2:
                    metrics['roc_auc'] = roc_auc_score(y_true, y_prob[:, 1])
                else:
                    metrics['roc_auc_ovr'] = roc_auc_score(
                        y_true, y_prob, multi_class='ovr', average='weighted'
                    )
            except Exception as e:
                logger.warning(f"Could not calculate ROC AUC: {e}")
        
        return metrics
    
    @staticmethod
    def evaluate_regression(
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict:
        """
        Evaluate regression model performance.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of evaluation metrics
        """
        metrics = {
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred),
            'r2': r2_score(y_true, y_pred),
            'mape': np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100,
        }
        
        # Directional accuracy (for time series)
        if len(y_true) > 1:
            true_direction = np.diff(y_true) > 0
            pred_direction = np.diff(y_pred) > 0
            directional_accuracy = np.mean(true_direction == pred_direction)
            metrics['directional_accuracy'] = directional_accuracy
        
        return metrics
    
    @staticmethod
    def evaluate_forecast(
        actual: np.ndarray,
        forecast: np.ndarray,
        confidence_lower: Optional[np.ndarray] = None,
        confidence_upper: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Evaluate forecast performance with confidence intervals.
        
        Args:
            actual: Actual values
            forecast: Forecasted values
            confidence_lower: Lower confidence bound
            confidence_upper: Upper confidence bound
            
        Returns:
            Dictionary of evaluation metrics
        """
        metrics = ModelEvaluator.evaluate_regression(actual, forecast)
        
        # Coverage probability (percentage of actual within confidence interval)
        if confidence_lower is not None and confidence_upper is not None:
            within_bounds = (actual >= confidence_lower) & (actual <= confidence_upper)
            metrics['coverage_probability'] = np.mean(within_bounds)
            metrics['interval_width_mean'] = np.mean(confidence_upper - confidence_lower)
        
        # Bias
        metrics['bias'] = np.mean(forecast - actual)
        
        return metrics
    
    @staticmethod
    def cross_validation_score(
        model,
        X: np.ndarray,
        y: np.ndarray,
        cv_folds: int = 5,
        task: str = 'classification'
    ) -> Dict:
        """
        Perform cross-validation and return scores.
        
        Args:
            model: ML model with fit/predict methods
            X: Feature matrix
            y: Target vector
            cv_folds: Number of CV folds
            task: 'classification' or 'regression'
            
        Returns:
            Dictionary of CV scores
        """
        from sklearn.model_selection import KFold
        
        kf = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
        scores = []
        
        for train_idx, val_idx in kf.split(X):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            
            if task == 'classification':
                score = f1_score(y_val, y_pred, average='weighted', zero_division=0)
            else:
                score = -mean_squared_error(y_val, y_pred)  # Negative for consistency
            
            scores.append(score)
        
        return {
            'cv_scores': scores,
            'cv_mean': np.mean(scores),
            'cv_std': np.std(scores)
        }
    
    @staticmethod
    def print_classification_report(metrics: Dict) -> None:
        """
        Print formatted classification report.
        
        Args:
            metrics: Metrics dictionary from evaluate_classification
        """
        print("\n" + "="*60)
        print("CLASSIFICATION MODEL EVALUATION")
        print("="*60)
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision (macro): {metrics['precision_macro']:.4f}")
        print(f"Recall (macro): {metrics['recall_macro']:.4f}")
        print(f"F1-Score (macro): {metrics['f1_macro']:.4f}")
        
        if 'roc_auc' in metrics:
            print(f"ROC AUC: {metrics['roc_auc']:.4f}")
        
        print("\nConfusion Matrix:")
        cm = np.array(metrics['confusion_matrix'])
        print(cm)
        
        print("\nPer-Class Metrics:")
        for class_name, class_metrics in metrics['per_class'].items():
            if class_name not in ['accuracy', 'macro avg', 'weighted avg']:
                print(f"  {class_name}: Precision={class_metrics['precision']:.4f}, "
                      f"Recall={class_metrics['recall']:.4f}, "
                      f"F1={class_metrics['f1-score']:.4f}")
        print("="*60)
    
    @staticmethod
    def print_regression_report(metrics: Dict) -> None:
        """
        Print formatted regression report.
        
        Args:
            metrics: Metrics dictionary from evaluate_regression
        """
        print("\n" + "="*60)
        print("REGRESSION MODEL EVALUATION")
        print("="*60)
        print(f"MSE: {metrics['mse']:.4f}")
        print(f"RMSE: {metrics['rmse']:.4f}")
        print(f"MAE: {metrics['mae']:.4f}")
        print(f"R²: {metrics['r2']:.4f}")
        print(f"MAPE: {metrics['mape']:.2f}%")
        
        if 'directional_accuracy' in metrics:
            print(f"Directional Accuracy: {metrics['directional_accuracy']:.4f}")
        print("="*60)


def compare_models(
    models: Dict[str, any],
    X_test: np.ndarray,
    y_test: np.ndarray,
    task: str = 'classification'
) -> Dict[str, Dict]:
    """
    Compare multiple models on test data.
    
    Args:
        models: Dictionary of model_name -> model
        X_test: Test features
        y_test: Test targets
        task: 'classification' or 'regression'
        
    Returns:
        Dictionary of model_name -> metrics
    """
    results = {}
    evaluator = ModelEvaluator()
    
    for name, model in models.items():
        y_pred = model.predict(X_test)
        
        if task == 'classification':
            y_prob = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
            metrics = evaluator.evaluate_classification(y_test, y_pred, y_prob)
        else:
            metrics = evaluator.evaluate_regression(y_test, y_pred)
        
        results[name] = metrics
    
    return results
