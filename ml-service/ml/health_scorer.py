"""
FinGuard AI - Financial Health Scorer
Rule-based and ML-enhanced financial health assessment
"""

import logging
from typing import Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class FinancialHealthScorer:
    """
    Financial health scoring system combining rule-based and ML approaches.
    Calculates overall score (0-100) with category breakdowns.
    """
    
    # Score weights for different categories
    WEIGHTS = {
        'savings': 0.30,
        'debt': 0.25,
        'investment': 0.20,
        'expense_stability': 0.15,
        'emergency_fund': 0.10
    }
    
    # Benchmark values
    BENCHMARKS = {
        'savings_rate': 0.20,  # 20% of income
        'debt_to_income': 0.30,  # 30% of income
        'investment_rate': 0.10,  # 10% of income
        'emergency_months': 6  # 6 months of expenses
    }
    
    def __init__(self):
        """Initialize the financial health scorer."""
        self.score_history = []
    
    def calculate_score(
        self,
        monthly_income: float,
        monthly_expenses: float,
        total_savings: float,
        total_debt: float,
        monthly_investments: float,
        emergency_fund: float,
        expense_trend_3m: List[float],
        age: Optional[int] = None
    ) -> Dict:
        """
        Calculate comprehensive financial health score.
        
        Args:
            monthly_income: Monthly income amount
            monthly_expenses: Monthly expense amount
            total_savings: Total savings amount
            total_debt: Total debt amount
            monthly_investments: Monthly investment amount
            emergency_fund: Emergency fund amount
            expense_trend_3m: Expense trend for last 3 months
            age: User age (optional)
            
        Returns:
            Financial health assessment with scores and recommendations
        """
        # Calculate individual scores
        savings_score = self._calculate_savings_score(
            monthly_income, monthly_expenses, total_savings
        )
        
        debt_score = self._calculate_debt_score(total_debt, monthly_income)
        
        investment_score = self._calculate_investment_score(
            monthly_investments, monthly_income, age
        )
        
        expense_stability_score = self._calculate_expense_stability_score(
            expense_trend_3m
        )
        
        emergency_fund_score = self._calculate_emergency_fund_score(
            emergency_fund, monthly_expenses
        )
        
        # Calculate weighted overall score
        overall_score = (
            savings_score * self.WEIGHTS['savings'] +
            debt_score * self.WEIGHTS['debt'] +
            investment_score * self.WEIGHTS['investment'] +
            expense_stability_score * self.WEIGHTS['expense_stability'] +
            emergency_fund_score * self.WEIGHTS['emergency_fund']
        )
        
        overall_score = int(round(overall_score))
        
        # Determine grade
        grade = self._determine_grade(overall_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            savings_score, debt_score, investment_score,
            emergency_fund_score, monthly_income, monthly_expenses,
            total_debt, monthly_investments
        )
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(
            savings_score, debt_score, investment_score,
            emergency_fund_score, monthly_income, monthly_expenses,
            total_debt, emergency_fund
        )
        
        return {
            'overall_score': overall_score,
            'grade': grade,
            'breakdown': {
                'savings_score': int(savings_score),
                'debt_score': int(debt_score),
                'investment_score': int(investment_score),
                'expense_stability_score': int(expense_stability_score),
                'emergency_fund_score': int(emergency_fund_score)
            },
            'recommendations': recommendations,
            'risk_factors': risk_factors
        }
    
    def _calculate_savings_score(
        self,
        monthly_income: float,
        monthly_expenses: float,
        total_savings: float
    ) -> float:
        """Calculate savings score (0-100)."""
        if monthly_income <= 0:
            return 0.0
        
        monthly_savings = monthly_income - monthly_expenses
        savings_rate = monthly_savings / monthly_income
        
        # Score based on savings rate
        if savings_rate >= 0.30:
            score = 100
        elif savings_rate >= 0.20:
            score = 80 + (savings_rate - 0.20) * 200
        elif savings_rate >= 0.10:
            score = 60 + (savings_rate - 0.10) * 200
        elif savings_rate >= 0.05:
            score = 40 + (savings_rate - 0.05) * 400
        else:
            score = max(0, savings_rate * 800)
        
        # Bonus for accumulated savings (up to 6 months expenses)
        months_saved = total_savings / monthly_expenses if monthly_expenses > 0 else 0
        savings_bonus = min(10, months_saved * 1.5)
        
        return min(100, score + savings_bonus)
    
    def _calculate_debt_score(
        self,
        total_debt: float,
        monthly_income: float
    ) -> float:
        """Calculate debt score (0-100)."""
        if monthly_income <= 0:
            return 50.0
        
        debt_to_income = total_debt / monthly_income
        
        # Score based on debt-to-income ratio
        if debt_to_income == 0:
            return 100.0
        elif debt_to_income <= 0.20:
            return 90.0
        elif debt_to_income <= 0.30:
            return 80 - (debt_to_income - 0.20) * 100
        elif debt_to_income <= 0.40:
            return 70 - (debt_to_income - 0.30) * 200
        elif debt_to_income <= 0.50:
            return 50 - (debt_to_income - 0.40) * 300
        else:
            return max(0, 20 - (debt_to_income - 0.50) * 40)
    
    def _calculate_investment_score(
        self,
        monthly_investments: float,
        monthly_income: float,
        age: Optional[int]
    ) -> float:
        """Calculate investment score (0-100)."""
        if monthly_income <= 0:
            return 0.0
        
        investment_rate = monthly_investments / monthly_income
        
        # Adjust target based on age
        target_rate = 0.10  # 10% default
        if age:
            if age < 30:
                target_rate = 0.15  # Higher when young
            elif age > 50:
                target_rate = 0.20  # Even higher near retirement
        
        # Score based on investment rate
        if investment_rate >= target_rate:
            score = 100
        elif investment_rate >= target_rate * 0.75:
            score = 80 + (investment_rate / target_rate - 0.75) * 80
        elif investment_rate >= target_rate * 0.50:
            score = 60 + (investment_rate / target_rate - 0.50) * 80
        elif investment_rate >= target_rate * 0.25:
            score = 40 + (investment_rate / target_rate - 0.25) * 80
        else:
            score = max(0, investment_rate / target_rate * 160)
        
        return min(100, score)
    
    def _calculate_expense_stability_score(
        self,
        expense_trend_3m: List[float]
    ) -> float:
        """Calculate expense stability score (0-100)."""
        if len(expense_trend_3m) < 2:
            return 70.0  # Neutral score for insufficient data
        
        expenses = np.array(expense_trend_3m)
        
        # Calculate coefficient of variation
        mean_expense = np.mean(expenses)
        if mean_expense == 0:
            return 100.0
        
        std_expense = np.std(expenses)
        cv = std_expense / mean_expense
        
        # Score inversely proportional to CV
        if cv <= 0.05:
            score = 100
        elif cv <= 0.10:
            score = 90 - (cv - 0.05) * 200
        elif cv <= 0.20:
            score = 80 - (cv - 0.10) * 300
        elif cv <= 0.30:
            score = 50 - (cv - 0.20) * 400
        else:
            score = max(0, 10 - (cv - 0.30) * 20)
        
        # Check trend direction
        if len(expenses) >= 3:
            if expenses[-1] > expenses[0] * 1.1:  # Increasing trend
                score *= 0.9
            elif expenses[-1] < expenses[0] * 0.9:  # Decreasing trend
                score *= 1.1
        
        return min(100, score)
    
    def _calculate_emergency_fund_score(
        self,
        emergency_fund: float,
        monthly_expenses: float
    ) -> float:
        """Calculate emergency fund score (0-100)."""
        if monthly_expenses <= 0:
            return 50.0
        
        months_covered = emergency_fund / monthly_expenses
        target_months = self.BENCHMARKS['emergency_months']
        
        # Score based on months covered
        if months_covered >= target_months:
            score = 100
        elif months_covered >= target_months * 0.75:
            score = 80 + (months_covered / target_months - 0.75) * 80
        elif months_covered >= target_months * 0.50:
            score = 60 + (months_covered / target_months - 0.50) * 80
        elif months_covered >= target_months * 0.25:
            score = 40 + (months_covered / target_months - 0.25) * 80
        else:
            score = max(0, months_covered / target_months * 160)
        
        return min(100, score)
    
    def _determine_grade(self, score: int) -> str:
        """Determine letter grade from score."""
        if score >= 85:
            return 'EXCELLENT'
        elif score >= 70:
            return 'GOOD'
        elif score >= 50:
            return 'FAIR'
        else:
            return 'POOR'
    
    def _generate_recommendations(
        self,
        savings_score: float,
        debt_score: float,
        investment_score: float,
        emergency_fund_score: float,
        monthly_income: float,
        monthly_expenses: float,
        total_debt: float,
        monthly_investments: float
    ) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        # Savings recommendations
        if savings_score < 60:
            target_savings = monthly_income * 0.20
            current_savings = monthly_income - monthly_expenses
            increase = target_savings - current_savings
            if increase > 0:
                recommendations.append(
                    f"Increase monthly savings by ₹{increase:,.0f} to reach 20% savings rate."
                )
        elif savings_score >= 80:
            recommendations.append(
                "Great savings habits! Consider increasing investments for long-term growth."
            )
        
        # Debt recommendations
        if debt_score < 60:
            recommendations.append(
                "Focus on paying down high-interest debt to improve financial health."
            )
        elif debt_score >= 80 and total_debt > 0:
            recommendations.append(
                "Your debt is well-managed. Continue making regular payments."
            )
        
        # Investment recommendations
        if investment_score < 60:
            target_investment = monthly_income * 0.10
            increase = target_investment - monthly_investments
            if increase > 0:
                recommendations.append(
                    f"Consider increasing monthly investments by ₹{increase:,.0f}."
                )
        elif investment_score >= 80:
            recommendations.append(
                "Excellent investment habits! Your future self will thank you."
            )
        
        # Emergency fund recommendations
        if emergency_fund_score < 60:
            target_fund = monthly_expenses * 6
            recommendations.append(
                f"Build emergency fund to ₹{target_fund:,.0f} (6 months of expenses)."
            )
        
        return recommendations
    
    def _identify_risk_factors(
        self,
        savings_score: float,
        debt_score: float,
        investment_score: float,
        emergency_fund_score: float,
        monthly_income: float,
        monthly_expenses: float,
        total_debt: float,
        emergency_fund: float
    ) -> List[str]:
        """Identify financial risk factors."""
        risks = []
        
        if savings_score < 50:
            risks.append("Low savings rate may impact long-term financial security.")
        
        if debt_score < 50:
            debt_ratio = total_debt / monthly_income if monthly_income > 0 else 0
            risks.append(f"High debt burden (DTI: {debt_ratio:.1%}) may limit financial flexibility.")
        
        if emergency_fund_score < 50:
            months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
            risks.append(f"Insufficient emergency fund ({months:.1f} months coverage).")
        
        if investment_score < 40:
            risks.append("Low investment rate may impact long-term wealth accumulation.")
        
        return risks


def calculate_financial_health(
    monthly_income: float,
    monthly_expenses: float,
    total_savings: float,
    total_debt: float,
    monthly_investments: float,
    emergency_fund: float,
    expense_trend_3m: List[float],
    age: Optional[int] = None
) -> Dict:
    """
    Convenience function for financial health calculation.
    
    Args:
        monthly_income: Monthly income amount
        monthly_expenses: Monthly expense amount
        total_savings: Total savings amount
        total_debt: Total debt amount
        monthly_investments: Monthly investment amount
        emergency_fund: Emergency fund amount
        expense_trend_3m: Expense trend for last 3 months
        age: User age (optional)
        
    Returns:
        Financial health assessment
    """
    scorer = FinancialHealthScorer()
    return scorer.calculate_score(
        monthly_income, monthly_expenses, total_savings,
        total_debt, monthly_investments, emergency_fund,
        expense_trend_3m, age
    )
