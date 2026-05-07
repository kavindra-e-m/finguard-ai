"""
FinGuard AI - Data Preprocessor
Utilities for data preprocessing and transformation
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocessor for financial data."""
    
    def __init__(self):
        """Initialize preprocessor with scalers and encoders."""
        self.scaler = StandardScaler()
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.is_fitted = False
    
    def fit_transform(
        self, 
        df: pd.DataFrame, 
        numeric_columns: List[str],
        categorical_columns: List[str]
    ) -> pd.DataFrame:
        """
        Fit preprocessor and transform data.
        
        Args:
            df: Input DataFrame
            numeric_columns: List of numeric column names
            categorical_columns: List of categorical column names
            
        Returns:
            Transformed DataFrame
        """
        result = df.copy()
        
        # Scale numeric columns
        if numeric_columns:
            result[numeric_columns] = self.scaler.fit_transform(
                result[numeric_columns]
            )
        
        # Encode categorical columns
        for col in categorical_columns:
            if col in result.columns:
                encoder = LabelEncoder()
                result[col] = encoder.fit_transform(result[col].astype(str))
                self.label_encoders[col] = encoder
        
        self.is_fitted = True
        return result
    
    def transform(
        self, 
        df: pd.DataFrame, 
        numeric_columns: List[str],
        categorical_columns: List[str]
    ) -> pd.DataFrame:
        """
        Transform data using fitted preprocessor.
        
        Args:
            df: Input DataFrame
            numeric_columns: List of numeric column names
            categorical_columns: List of categorical column names
            
        Returns:
            Transformed DataFrame
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        result = df.copy()
        
        # Scale numeric columns
        if numeric_columns:
            result[numeric_columns] = self.scaler.transform(
                result[numeric_columns]
            )
        
        # Encode categorical columns
        for col in categorical_columns:
            if col in result.columns and col in self.label_encoders:
                encoder = self.label_encoders[col]
                # Handle unseen categories
                result[col] = result[col].astype(str).apply(
                    lambda x: encoder.transform([x])[0] 
                    if x in encoder.classes_ else -1
                )
        
        return result
    
    def handle_missing_values(
        self, 
        df: pd.DataFrame, 
        strategy: str = 'mean'
    ) -> pd.DataFrame:
        """
        Handle missing values in DataFrame.
        
        Args:
            df: Input DataFrame
            strategy: Imputation strategy ('mean', 'median', 'mode', 'drop')
            
        Returns:
            DataFrame with handled missing values
        """
        result = df.copy()
        
        if strategy == 'drop':
            return result.dropna()
        
        for col in result.columns:
            if result[col].isnull().any():
                if result[col].dtype in ['int64', 'float64']:
                    if strategy == 'mean':
                        fill_value = result[col].mean()
                    elif strategy == 'median':
                        fill_value = result[col].median()
                    else:
                        fill_value = result[col].mode()[0]
                else:
                    fill_value = result[col].mode()[0] if not result[col].mode().empty else 'Unknown'
                
                result[col] = result[col].fillna(fill_value)
        
        return result
    
    def remove_outliers(
        self, 
        df: pd.DataFrame, 
        columns: List[str],
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        Remove outliers from DataFrame.
        
        Args:
            df: Input DataFrame
            columns: Columns to check for outliers
            method: Outlier detection method ('iqr' or 'zscore')
            threshold: Threshold for outlier detection
            
        Returns:
            DataFrame with outliers removed
        """
        result = df.copy()
        mask = pd.Series([True] * len(result), index=result.index)
        
        for col in columns:
            if col not in result.columns:
                continue
                
            if method == 'iqr':
                Q1 = result[col].quantile(0.25)
                Q3 = result[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                col_mask = (result[col] >= lower_bound) & (result[col] <= upper_bound)
            else:  # zscore
                z_scores = np.abs((result[col] - result[col].mean()) / result[col].std())
                col_mask = z_scores < threshold
            
            mask = mask & col_mask
        
        return result[mask]
    
    def create_time_features(self, df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        Create time-based features from date column.
        
        Args:
            df: Input DataFrame
            date_column: Name of date column
            
        Returns:
            DataFrame with additional time features
        """
        result = df.copy()
        result[date_column] = pd.to_datetime(result[date_column])
        
        result['year'] = result[date_column].dt.year
        result['month'] = result[date_column].dt.month
        result['day'] = result[date_column].dt.day
        result['day_of_week'] = result[date_column].dt.dayofweek
        result['day_of_year'] = result[date_column].dt.dayofyear
        result['week_of_year'] = result[date_column].dt.isocalendar().week
        result['quarter'] = result[date_column].dt.quarter
        result['is_weekend'] = result[date_column].dt.dayofweek.isin([5, 6]).astype(int)
        result['is_month_start'] = result[date_column].dt.is_month_start.astype(int)
        result['is_month_end'] = result[date_column].dt.is_month_end.astype(int)
        
        return result


def normalize_features(
    features: np.ndarray, 
    method: str = 'minmax'
) -> np.ndarray:
    """
    Normalize feature array.
    
    Args:
        features: Input feature array
        method: Normalization method ('minmax' or 'standard')
        
    Returns:
        Normalized features
    """
    if method == 'minmax':
        min_val = features.min(axis=0)
        max_val = features.max(axis=0)
        return (features - min_val) / (max_val - min_val + 1e-8)
    else:  # standard
        mean = features.mean(axis=0)
        std = features.std(axis=0)
        return (features - mean) / (std + 1e-8)


def create_lag_features(
    df: pd.DataFrame, 
    column: str, 
    lags: List[int]
) -> pd.DataFrame:
    """
    Create lag features for time series data.
    
    Args:
        df: Input DataFrame
        column: Column to create lags for
        lags: List of lag periods
        
    Returns:
        DataFrame with lag features
    """
    result = df.copy()
    
    for lag in lags:
        result[f'{column}_lag_{lag}'] = result[column].shift(lag)
    
    return result


def create_rolling_features(
    df: pd.DataFrame, 
    column: str, 
    windows: List[int],
    aggregations: List[str] = ['mean', 'std', 'min', 'max']
) -> pd.DataFrame:
    """
    Create rolling window features.
    
    Args:
        df: Input DataFrame
        column: Column to create rolling features for
        windows: List of window sizes
        aggregations: List of aggregation functions
        
    Returns:
        DataFrame with rolling features
    """
    result = df.copy()
    
    for window in windows:
        for agg in aggregations:
            col_name = f'{column}_rolling_{window}_{agg}'
            if agg == 'mean':
                result[col_name] = result[column].rolling(window=window).mean()
            elif agg == 'std':
                result[col_name] = result[column].rolling(window=window).std()
            elif agg == 'min':
                result[col_name] = result[column].rolling(window=window).min()
            elif agg == 'max':
                result[col_name] = result[column].rolling(window=window).max()
    
    return result
