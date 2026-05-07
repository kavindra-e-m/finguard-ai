"""
FinGuard AI - Portfolio Optimizer
Markowitz Mean-Variance optimization using PyPortfolioOpt
"""

import logging
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.base_optimizer import BaseOptimizer

logger = logging.getLogger(__name__)


class PortfolioOptimizer:
    """
    Portfolio optimizer using Markowitz Modern Portfolio Theory.
    Optimizes asset allocation based on risk tolerance and investment goals.
    """
    
    # Asset class expected annual returns (based on historical data)
    ASSET_RETURNS = {
        'STOCKS': 0.12,        # 12% expected return
        'MUTUAL_FUNDS': 0.10,  # 10% expected return
        'BONDS': 0.06,         # 6% expected return
        'GOLD': 0.08,          # 8% expected return
        'CRYPTO': 0.20,        # 20% expected return (high volatility)
        'FD': 0.07             # 7% fixed deposit return
    }
    
    # Asset class annual volatilities (standard deviation)
    ASSET_VOLATILITIES = {
        'STOCKS': 0.16,
        'MUTUAL_FUNDS': 0.12,
        'BONDS': 0.04,
        'GOLD': 0.15,
        'CRYPTO': 0.50,
        'FD': 0.01
    }
    
    # Correlation matrix between asset classes
    CORRELATION_MATRIX = np.array([
        [1.00, 0.80, 0.20, 0.30, 0.40, 0.10],  # STOCKS
        [0.80, 1.00, 0.30, 0.35, 0.35, 0.15],  # MUTUAL_FUNDS
        [0.20, 0.30, 1.00, 0.10, -0.10, 0.05], # BONDS
        [0.30, 0.35, 0.10, 1.00, 0.20, 0.00],  # GOLD
        [0.40, 0.35, -0.10, 0.20, 1.00, 0.00], # CRYPTO
        [0.10, 0.15, 0.05, 0.00, 0.00, 1.00]   # FD
    ])
    
    ASSET_CLASSES = ['STOCKS', 'MUTUAL_FUNDS', 'BONDS', 'GOLD', 'CRYPTO', 'FD']
    
    def __init__(self, risk_free_rate: float = 0.06):
        """
        Initialize the portfolio optimizer.
        
        Args:
            risk_free_rate: Annual risk-free rate (default 6%)
        """
        self.risk_free_rate = risk_free_rate
        self._build_covariance_matrix()
    
    def _build_covariance_matrix(self) -> None:
        """Build the covariance matrix from volatilities and correlations."""
        volatilities = np.array([
            self.ASSET_VOLATILITIES[asset] 
            for asset in self.ASSET_CLASSES
        ])
        
        # Covariance matrix: σ_ij = ρ_ij * σ_i * σ_j
        self.cov_matrix = np.outer(volatilities, volatilities) * self.CORRELATION_MATRIX
        
        # Convert to DataFrame for PyPortfolioOpt
        self.cov_df = pd.DataFrame(
            self.cov_matrix,
            index=self.ASSET_CLASSES,
            columns=self.ASSET_CLASSES
        )
        
        # Expected returns as Series
        self.expected_returns = pd.Series(
            {asset: self.ASSET_RETURNS[asset] for asset in self.ASSET_CLASSES}
        )
    
    def optimize(
        self,
        risk_tolerance: str,
        available_capital: float,
        investment_horizon_years: int = 5,
        constraints: Optional[Dict[str, tuple]] = None
    ) -> Dict:
        """
        Optimize portfolio based on risk tolerance.
        
        Args:
            risk_tolerance: Risk level - 'LOW', 'MEDIUM', or 'HIGH'
            available_capital: Total capital available for investment
            investment_horizon_years: Investment time horizon
            constraints: Optional asset weight constraints
            
        Returns:
            Optimization results with weights and performance metrics
        """
        risk_tolerance = risk_tolerance.upper()
        
        # Adjust returns based on investment horizon
        adjusted_returns = self._adjust_returns_for_horizon(
            self.expected_returns, investment_horizon_years
        )
        
        # Create efficient frontier
        ef = EfficientFrontier(adjusted_returns, self.cov_df)
        
        # Apply constraints
        if constraints:
            for asset, (min_w, max_w) in constraints.items():
                if asset in self.ASSET_CLASSES:
                    ef.add_constraint(lambda w, a=asset, min_w=min_w, max_w=max_w: 
                        w[self.ASSET_CLASSES.index(a)] >= min_w)
                    ef.add_constraint(lambda w, a=asset, min_w=min_w, max_w=max_w: 
                        w[self.ASSET_CLASSES.index(a)] <= max_w)
        
        # Optimize based on risk tolerance
        if risk_tolerance == 'LOW':
            # Minimize volatility
            weights = ef.min_volatility()
        elif risk_tolerance == 'HIGH':
            # Maximize return with higher risk tolerance
            ef.add_constraint(lambda w: w @ self.cov_df @ w <= 0.20)  # Max 20% volatility
            weights = ef.max_sharpe(risk_free_rate=self.risk_free_rate)
        else:  # MEDIUM
            # Maximize Sharpe ratio
            weights = ef.max_sharpe(risk_free_rate=self.risk_free_rate)
        
        # Clean weights (remove very small allocations)
        cleaned_weights = ef.clean_weights()
        
        # Calculate portfolio performance
        performance = ef.portfolio_performance(risk_free_rate=self.risk_free_rate)
        
        # Format results
        result = self._format_results(
            cleaned_weights, performance, available_capital, risk_tolerance
        )
        
        return result
    
    def _adjust_returns_for_horizon(
        self, 
        returns: pd.Series, 
        years: int
    ) -> pd.Series:
        """
        Adjust expected returns based on investment horizon.
        
        Args:
            returns: Annual expected returns
            years: Investment horizon in years
            
        Returns:
            Adjusted returns
        """
        # Longer horizons can tolerate more volatility, slightly higher expected returns
        adjustment_factor = 1 + (years - 5) * 0.01  # 1% per year deviation from 5-year base
        adjustment_factor = max(0.95, min(1.10, adjustment_factor))  # Cap adjustments
        
        return returns * adjustment_factor
    
    def _format_results(
        self,
        weights: Dict[str, float],
        performance: tuple,
        capital: float,
        risk_label: str
    ) -> Dict:
        """
        Format optimization results.
        
        Args:
            weights: Asset weights
            performance: (expected_return, volatility, sharpe_ratio)
            capital: Available capital
            risk_label: Risk tolerance label
            
        Returns:
            Formatted results dictionary
        """
        expected_return, volatility, sharpe_ratio = performance
        
        # Calculate allocation amounts
        allocation_amounts = {
            asset: round(weight * capital, 2)
            for asset, weight in weights.items()
        }
        
        # Filter out zero allocations
        non_zero_weights = {k: round(v, 4) for k, v in weights.items() if v > 0.001}
        non_zero_amounts = {k: v for k, v in allocation_amounts.items() if v > 0}
        
        return {
            'weights': non_zero_weights,
            'allocation_amounts': non_zero_amounts,
            'expected_annual_return': round(expected_return, 4),
            'annual_volatility': round(volatility, 4),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'risk_label': risk_label
        }
    
    def get_efficient_frontier_points(
        self,
        n_points: int = 50
    ) -> Dict[str, List[float]]:
        """
        Generate points along the efficient frontier.
        
        Args:
            n_points: Number of points to generate
            
        Returns:
            Dictionary with volatility and return points
        """
        ef = EfficientFrontier(self.expected_returns, self.cov_df)
        
        # Get min volatility portfolio
        ef.min_volatility()
        min_vol_perf = ef.portfolio_performance()
        
        # Get max return portfolio
        ef = EfficientFrontier(self.expected_returns, self.cov_df)
        # Maximize return without constraints
        target_returns = np.linspace(min_vol_perf[0], self.expected_returns.max() * 0.9, n_points)
        
        volatilities = []
        returns = []
        
        for target in target_returns:
            try:
                ef = EfficientFrontier(self.expected_returns, self.cov_df)
                ef.efficient_return(target)
                perf = ef.portfolio_performance()
                returns.append(perf[0])
                volatilities.append(perf[1])
            except Exception:
                pass
        
        return {
            'volatilities': volatilities,
            'returns': returns
        }


def optimize_portfolio(
    risk_tolerance: str,
    available_capital: float,
    investment_horizon_years: int = 5
) -> Dict:
    """
    Convenience function for portfolio optimization.
    
    Args:
        risk_tolerance: Risk level - 'LOW', 'MEDIUM', or 'HIGH'
        available_capital: Total capital available
        investment_horizon_years: Investment time horizon
        
    Returns:
        Portfolio optimization results
    """
    optimizer = PortfolioOptimizer()
    return optimizer.optimize(risk_tolerance, available_capital, investment_horizon_years)


def get_asset_info() -> Dict[str, Dict]:
    """
    Get information about available asset classes.
    
    Returns:
        Dictionary with asset class information
    """
    optimizer = PortfolioOptimizer()
    
    return {
        asset: {
            'expected_return': optimizer.ASSET_RETURNS[asset],
            'volatility': optimizer.ASSET_VOLATILITIES[asset],
            'description': _get_asset_description(asset)
        }
        for asset in optimizer.ASSET_CLASSES
    }


def _get_asset_description(asset: str) -> str:
    """Get description for asset class."""
    descriptions = {
        'STOCKS': 'Direct equity investments in publicly traded companies',
        'MUTUAL_FUNDS': 'Diversified professionally managed investment funds',
        'BONDS': 'Fixed income securities with regular interest payments',
        'GOLD': 'Precious metal investment for portfolio diversification',
        'CRYPTO': 'Digital currency investments with high volatility',
        'FD': 'Fixed deposits with guaranteed returns and low risk'
    }
    return descriptions.get(asset, 'Investment asset')
