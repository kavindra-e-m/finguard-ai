"""
FinGuard AI - Expense Predictor
Time series forecasting for expense prediction using Prophet and Linear Regression
"""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.linear_model import LinearRegression

logger = logging.getLogger(__name__)


class ExpensePredictor:
    """
    Expense prediction model using Prophet for time series forecasting
    with Linear Regression as a baseline comparison.
    """
    
    def __init__(self):
        """Initialize the expense predictor."""
        self.prophet_model: Optional[Prophet] = None
        self.lr_model: Optional[LinearRegression] = None
        self.is_trained = False
        self.last_values: List[float] = []
    
    def prepare_data(
        self, 
        monthly_expenses: List[Dict[str, any]]
    ) -> pd.DataFrame:
        """
        Prepare expense data for modeling.
        
        Args:
            monthly_expenses: List of {month: str, amount: float} dictionaries
            
        Returns:
            Prepared DataFrame
        """
        df = pd.DataFrame(monthly_expenses)
        df['ds'] = pd.to_datetime(df['month'])
        df['y'] = df['amount'].astype(float)
        df = df.sort_values('ds')
        
        return df[['ds', 'y']]
    
    def train(
        self, 
        monthly_expenses: List[Dict[str, any]],
        use_prophet: bool = True
    ) -> None:
        """
        Train the expense prediction models.
        
        Args:
            monthly_expenses: List of monthly expense data
            use_prophet: Whether to train Prophet model
        """
        if len(monthly_expenses) < 3:
            logger.warning("Insufficient data for training. Need at least 3 months.")
            return
        
        df = self.prepare_data(monthly_expenses)
        self.last_values = df['y'].tolist()
        
        # Train Prophet model
        if use_prophet and len(df) >= 6:
            try:
                self.prophet_model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    interval_width=0.95,
                    changepoint_prior_scale=0.05
                )
                self.prophet_model.fit(df)
                logger.info("Prophet model trained successfully")
            except Exception as e:
                logger.error(f"Failed to train Prophet model: {e}")
                self.prophet_model = None
        
        # Train Linear Regression as baseline
        try:
            X = np.arange(len(df)).reshape(-1, 1)
            y = df['y'].values
            
            self.lr_model = LinearRegression()
            self.lr_model.fit(X, y)
            logger.info("Linear Regression model trained successfully")
        except Exception as e:
            logger.error(f"Failed to train Linear Regression model: {e}")
            self.lr_model = None
        
        self.is_trained = True
    
    def predict(
        self, 
        periods: int = 3
    ) -> Dict:
        """
        Predict future expenses.
        
        Args:
            periods: Number of future periods to predict
            
        Returns:
            Dictionary with predictions and confidence intervals
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Default to simple extrapolation if models aren't available
        if self.prophet_model is None and self.lr_model is None:
            return self._simple_prediction(periods)
        
        # Use Prophet if available
        if self.prophet_model is not None:
            return self._prophet_prediction(periods)
        
        # Fall back to Linear Regression
        return self._lr_prediction(periods)
    
    def _prophet_prediction(self, periods: int) -> Dict:
        """Generate prediction using Prophet model."""
        try:
            future = self.prophet_model.make_future_dataframe(periods=periods, freq='MS')
            forecast = self.prophet_model.predict(future)
            
            # Get the last actual value and predictions
            last_actual_idx = len(self.last_values)
            predictions = forecast.iloc[last_actual_idx:last_actual_idx + periods]
            
            predicted_values = predictions['yhat'].tolist()
            lower_bounds = predictions['yhat_lower'].tolist()
            upper_bounds = predictions['yhat_upper'].tolist()
            
            # Determine trend
            trend = self._determine_trend(predicted_values)
            
            return {
                'predicted_next_month': round(predicted_values[0], 2),
                'confidence_lower': round(lower_bounds[0], 2),
                'confidence_upper': round(upper_bounds[0], 2),
                'trend': trend,
                'forecast_3_months': [round(v, 2) for v in predicted_values],
                'model_used': 'prophet'
            }
        except Exception as e:
            logger.error(f"Prophet prediction failed: {e}")
            return self._lr_prediction(periods)
    
    def _lr_prediction(self, periods: int) -> Dict:
        """Generate prediction using Linear Regression model."""
        try:
            n = len(self.last_values)
            X_future = np.arange(n, n + periods).reshape(-1, 1)
            predictions = self.lr_model.predict(X_future)
            
            # Calculate confidence interval based on historical residuals
            X_hist = np.arange(n).reshape(-1, 1)
            hist_predictions = self.lr_model.predict(X_hist)
            residuals = np.array(self.last_values) - hist_predictions
            std_residual = np.std(residuals)
            
            lower_bounds = predictions - 1.96 * std_residual
            upper_bounds = predictions + 1.96 * std_residual
            
            # Determine trend
            trend = self._determine_trend(predictions.tolist())
            
            return {
                'predicted_next_month': round(predictions[0], 2),
                'confidence_lower': round(max(0, lower_bounds[0]), 2),
                'confidence_upper': round(upper_bounds[0], 2),
                'trend': trend,
                'forecast_3_months': [round(v, 2) for v in predictions],
                'model_used': 'linear_regression'
            }
        except Exception as e:
            logger.error(f"Linear Regression prediction failed: {e}")
            return self._simple_prediction(periods)
    
    def _simple_prediction(self, periods: int) -> Dict:
        """Simple prediction using moving average when models fail."""
        if len(self.last_values) == 0:
            return {
                'predicted_next_month': 0,
                'confidence_lower': 0,
                'confidence_upper': 0,
                'trend': 'STABLE',
                'forecast_3_months': [0, 0, 0],
                'model_used': 'fallback'
            }
        
        # Use last 3-month moving average
        recent = self.last_values[-3:] if len(self.last_values) >= 3 else self.last_values
        avg = np.mean(recent)
        std = np.std(recent) if len(recent) > 1 else avg * 0.1
        
        predictions = [avg] * periods
        trend = self._determine_trend(self.last_values + predictions)
        
        return {
            'predicted_next_month': round(avg, 2),
            'confidence_lower': round(max(0, avg - 1.96 * std), 2),
            'confidence_upper': round(avg + 1.96 * std, 2),
            'trend': trend,
            'forecast_3_months': [round(v, 2) for v in predictions],
            'model_used': 'fallback'
        }
    
    def _determine_trend(self, values: List[float]) -> str:
        """
        Determine trend direction from values.
        
        Args:
            values: List of values
            
        Returns:
            Trend direction: 'INCREASING', 'DECREASING', or 'STABLE'
        """
        if len(values) < 2:
            return 'STABLE'
        
        # Use linear regression slope
        x = np.arange(len(values))
        y = np.array(values)
        
        n = len(x)
        slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (
            n * np.sum(x ** 2) - np.sum(x) ** 2 + 1e-8
        )
        
        mean_val = np.mean(y)
        if mean_val == 0:
            return 'STABLE'
        
        relative_slope = slope / mean_val
        
        if relative_slope > 0.05:
            return 'INCREASING'
        elif relative_slope < -0.05:
            return 'DECREASING'
        else:
            return 'STABLE'
    
    def save(self, filepath: str) -> None:
        """
        Save the trained models.
        
        Args:
            filepath: Path to save the model
        """
        import joblib
        
        model_data = {
            'prophet_model': self.prophet_model,
            'lr_model': self.lr_model,
            'last_values': self.last_values,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """
        Load trained models.
        
        Args:
            filepath: Path to load the model from
        """
        import joblib
        
        model_data = joblib.load(filepath)
        
        self.prophet_model = model_data.get('prophet_model')
        self.lr_model = model_data.get('lr_model')
        self.last_values = model_data.get('last_values', [])
        self.is_trained = model_data.get('is_trained', False)
        
        logger.info(f"Model loaded from {filepath}")


def predict_expense(
    monthly_expenses: List[Dict[str, any]],
    forecast_periods: int = 3
) -> Dict:
    """
    Convenience function for expense prediction.
    
    Args:
        monthly_expenses: List of monthly expense data
        forecast_periods: Number of periods to forecast
        
    Returns:
        Prediction results dictionary
    """
    predictor = ExpensePredictor()
    predictor.train(monthly_expenses)
    return predictor.predict(periods=forecast_periods)
