"""
FinGuard AI - Feature Engineering
Utilities for creating financial behavior features
"""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class FinancialFeatureEngineer:
    """Feature engineer for financial behavior analysis."""
    
    @staticmethod
    def calculate_savings_ratio(
        monthly_income: float, 
        monthly_expenses: float
    ) -> float:
        """
        Calculate savings ratio.
        
        Args:
            monthly_income: Monthly income amount
            monthly_expenses: Monthly expense amount
            
        Returns:
            Savings ratio (0-1)
        """
        if monthly_income <= 0:
            return 0.0
        savings = monthly_income - monthly_expenses
        return max(0.0, savings / monthly_income)
    
    @staticmethod
    def calculate_debt_to_income_ratio(
        total_debt: float, 
        monthly_income: float
    ) -> float:
        """
        Calculate debt-to-income ratio.
        
        Args:
            total_debt: Total debt amount
            monthly_income: Monthly income amount
            
        Returns:
            Debt-to-income ratio
        """
        if monthly_income <= 0:
            return 0.0
        return total_debt / monthly_income
    
    @staticmethod
    def calculate_expense_variability(
        monthly_expenses: List[float]
    ) -> float:
        """
        Calculate expense variability (coefficient of variation).
        
        Args:
            monthly_expenses: List of monthly expense amounts
            
        Returns:
            Expense variability ratio
        """
        if len(monthly_expenses) < 2:
            return 0.0
        
        expenses = np.array(monthly_expenses)
        mean = np.mean(expenses)
        
        if mean == 0:
            return 0.0
        
        std = np.std(expenses)
        return std / mean
    
    @staticmethod
    def calculate_expense_growth_rate(
        monthly_expenses: List[float]
    ) -> float:
        """
        Calculate expense growth rate.
        
        Args:
            monthly_expenses: List of monthly expense amounts
            
        Returns:
            Growth rate (positive = increasing, negative = decreasing)
        """
        if len(monthly_expenses) < 2:
            return 0.0
        
        # Use linear regression slope / mean
        x = np.arange(len(monthly_expenses))
        y = np.array(monthly_expenses)
        
        # Calculate slope using least squares
        n = len(x)
        slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (
            n * np.sum(x ** 2) - np.sum(x) ** 2
        )
        
        mean_expense = np.mean(y)
        if mean_expense == 0:
            return 0.0
        
        return slope / mean_expense
    
    @staticmethod
    def calculate_category_ratios(
        expenses_df: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate expense ratios by category.
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            Dictionary of category ratios
        """
        if expenses_df.empty:
            return {}
        
        total = expenses_df['amount'].sum()
        if total == 0:
            return {}
        
        category_sums = expenses_df.groupby('category')['amount'].sum()
        ratios = (category_sums / total).to_dict()
        
        return ratios
    
    @staticmethod
    def calculate_emergency_fund_months(
        emergency_fund: float, 
        monthly_expenses: float
    ) -> float:
        """
        Calculate emergency fund coverage in months.
        
        Args:
            emergency_fund: Emergency fund amount
            monthly_expenses: Monthly expense amount
            
        Returns:
            Number of months covered by emergency fund
        """
        if monthly_expenses <= 0:
            return float('inf') if emergency_fund > 0 else 0.0
        return emergency_fund / monthly_expenses
    
    @staticmethod
    def calculate_investment_rate(
        monthly_investments: float, 
        monthly_income: float
    ) -> float:
        """
        Calculate investment rate.
        
        Args:
            monthly_investments: Monthly investment amount
            monthly_income: Monthly income amount
            
        Returns:
            Investment rate (0-1)
        """
        if monthly_income <= 0:
            return 0.0
        return monthly_investments / monthly_income
    
    @staticmethod
    def calculate_risk_exposure(
        expenses_df: pd.DataFrame,
        high_risk_categories: List[str] = None
    ) -> float:
        """
        Calculate risk exposure from discretionary spending.
        
        Args:
            expenses_df: DataFrame with expense data
            high_risk_categories: List of high-risk categories
            
        Returns:
            Risk exposure ratio
        """
        if high_risk_categories is None:
            high_risk_categories = ['ENTERTAINMENT', 'SHOPPING', 'OTHER']
        
        if expenses_df.empty:
            return 0.0
        
        total = expenses_df['amount'].sum()
        if total == 0:
            return 0.0
        
        high_risk_spend = expenses_df[
            expenses_df['category'].isin(high_risk_categories)
        ]['amount'].sum()
        
        return high_risk_spend / total
    
    @staticmethod
    def calculate_avg_transaction_size(
        expenses_df: pd.DataFrame
    ) -> float:
        """
        Calculate average transaction size.
        
        Args:
            expenses_df: DataFrame with expense data
            
        Returns:
            Average transaction amount
        """
        if expenses_df.empty:
            return 0.0
        return expenses_df['amount'].mean()
    
    @staticmethod
    def calculate_income_stability_score(
        monthly_incomes: List[float]
    ) -> float:
        """
        Calculate income stability score.
        
        Args:
            monthly_incomes: List of monthly income amounts
            
        Returns:
            Stability score (0-1, higher is more stable)
        """
        if len(monthly_incomes) < 2:
            return 1.0
        
        incomes = np.array(monthly_incomes)
        mean = np.mean(incomes)
        
        if mean == 0:
            return 0.0
        
        std = np.std(incomes)
        cv = std / mean  # Coefficient of variation
        
        # Convert to stability score (inverse of CV, capped at 1)
        stability = max(0.0, 1.0 - cv)
        return stability
    
    @staticmethod
    def extract_personality_features(
        monthly_income: float,
        monthly_expenses: float,
        expenses_df: pd.DataFrame,
        total_savings: float,
        monthly_investments: float
    ) -> Dict[str, float]:
        """
        Extract features for personality detection.
        
        Args:
            monthly_income: Monthly income
            monthly_expenses: Monthly expenses
            expenses_df: Expense DataFrame
            total_savings: Total savings
            monthly_investments: Monthly investments
            
        Returns:
            Dictionary of personality features
        """
        savings_ratio = FinancialFeatureEngineer.calculate_savings_ratio(
            monthly_income, monthly_expenses
        )
        
        # Get monthly expense history for variability
        monthly_history = []
        if not expenses_df.empty and 'date' in expenses_df.columns:
            expenses_df['date'] = pd.to_datetime(expenses_df['date'])
            expenses_df['year_month'] = expenses_df['date'].dt.to_period('M')
            monthly_history = expenses_df.groupby('year_month')['amount'].sum().tolist()
        
        expense_variability = FinancialFeatureEngineer.calculate_expense_variability(
            monthly_history if monthly_history else [monthly_expenses]
        )
        
        # Investment frequency (approximate from monthly investment)
        investment_frequency = 1 if monthly_investments > 0 else 0
        
        # Risk exposure
        risk_exposure = FinancialFeatureEngineer.calculate_risk_exposure(expenses_df)
        
        # Category ratios
        category_ratios = FinancialFeatureEngineer.calculate_category_ratios(expenses_df)
        
        features = {
            'savings_ratio': savings_ratio,
            'expense_variability': expense_variability,
            'investment_frequency': investment_frequency,
            'risk_exposure': risk_exposure,
            'food_ratio': category_ratios.get('FOOD', 0.0),
            'entertainment_ratio': category_ratios.get('ENTERTAINMENT', 0.0),
            'avg_transaction': FinancialFeatureEngineer.calculate_avg_transaction_size(expenses_df),
            'monthly_income': monthly_income
        }
        
        return features
    
    @staticmethod
    def extract_stress_features(
        monthly_income: float,
        monthly_expenses: float,
        total_debt: float,
        emergency_fund: float,
        expenses_df: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Extract features for stress prediction.
        
        Args:
            monthly_income: Monthly income
            monthly_expenses: Monthly expenses
            total_debt: Total debt
            emergency_fund: Emergency fund
            expenses_df: Expense DataFrame
            
        Returns:
            Dictionary of stress features
        """
        debt_to_income = FinancialFeatureEngineer.calculate_debt_to_income_ratio(
            total_debt, monthly_income
        )
        
        savings_ratio = FinancialFeatureEngineer.calculate_savings_ratio(
            monthly_income, monthly_expenses
        )
        
        # Get expense growth rate
        monthly_history = []
        if not expenses_df.empty and 'date' in expenses_df.columns:
            expenses_df['date'] = pd.to_datetime(expenses_df['date'])
            expenses_df['year_month'] = expenses_df['date'].dt.to_period('M')
            monthly_history = expenses_df.groupby('year_month')['amount'].sum().tolist()
        
        expense_growth = FinancialFeatureEngineer.calculate_expense_growth_rate(
            monthly_history if len(monthly_history) >= 2 else [monthly_expenses] * 2
        )
        
        # Income stability (assume stable if no history)
        income_stability = 0.8
        
        # Emergency fund months
        emergency_months = FinancialFeatureEngineer.calculate_emergency_fund_months(
            emergency_fund, monthly_expenses
        )
        
        features = {
            'debt_to_income_ratio': debt_to_income,
            'savings_rate': savings_ratio,
            'expense_growth_rate': expense_growth,
            'income_stability_score': income_stability,
            'emergency_fund_months': emergency_months
        }
        
        return features
