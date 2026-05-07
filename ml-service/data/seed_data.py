"""
FinGuard AI - Seed Data Generator
Generates demo user and synthetic data for testing
"""

import logging
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd

try:
    import psycopg2
    from psycopg2.extras import DictCursor
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeedDataGenerator:
    """Generator for demo and seed data."""
    
    # Expense categories
    CATEGORIES = [
        'FOOD', 'TRANSPORT', 'BILLS', 'ENTERTAINMENT', 
        'HEALTHCARE', 'EDUCATION', 'SHOPPING', 'INVESTMENT', 'SAVINGS', 'OTHER'
    ]
    
    # Investment types
    INVESTMENT_TYPES = ['STOCKS', 'MUTUAL_FUNDS', 'BONDS', 'CRYPTO', 'GOLD', 'FD']
    
    def __init__(self, seed: int = 42):
        """Initialize the seed data generator."""
        random.seed(seed)
        np.random.seed(seed)
    
    def generate_demo_user(self) -> Dict:
        """Generate demo user data."""
        return {
            'id': 1,
            'name': 'Demo User',
            'email': 'demo@finguard.ai',
            'password': 'Demo@123',  # Plain text for demo only
            'monthly_income': 50000,
            'created_at': datetime.now().isoformat()
        }
    
    def generate_expenses(
        self, 
        user_id: int = 1, 
        months: int = 24,
        monthly_income: float = 50000
    ) -> List[Dict]:
        """
        Generate synthetic expense data with realistic patterns.
        
        Args:
            user_id: User ID
            months: Number of months of data
            monthly_income: Monthly income
            
        Returns:
            List of expense records
        """
        expenses = []
        expense_id = 1
        
        # Base monthly budget allocation (percentages)
        category_weights = {
            'FOOD': 0.28,
            'TRANSPORT': 0.12,
            'BILLS': 0.18,
            'ENTERTAINMENT': 0.12,
            'HEALTHCARE': 0.05,
            'EDUCATION': 0.05,
            'SHOPPING': 0.10,
            'INVESTMENT': 0.05,
            'SAVINGS': 0.03,
            'OTHER': 0.02
        }
        
        # Generate increasing trend to trigger stress detection
        base_expense = monthly_income * 0.65  # Start with 65% of income
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)
        
        for month_offset in range(months):
            month_date = start_date + timedelta(days=30 * month_offset)
            
            # Increase expenses over time (to trigger stress detection)
            trend_factor = 1 + (month_offset / months) * 0.15  # 15% increase over period
            month_budget = base_expense * trend_factor
            
            # Generate daily expenses for the month
            days_in_month = 30
            for day in range(1, days_in_month + 1):
                expense_date = month_date + timedelta(days=day - 1)
                
                # Skip some days (not every day has expenses)
                if random.random() > 0.7:
                    continue
                
                # Select category based on weights
                category = random.choices(
                    list(category_weights.keys()),
                    weights=list(category_weights.values())
                )[0]
                
                # Generate amount based on category
                if category == 'FOOD':
                    amount = random.uniform(150, 800)
                elif category == 'TRANSPORT':
                    amount = random.uniform(50, 500)
                elif category == 'BILLS':
                    amount = random.uniform(500, 3000) if day == 1 else 0
                elif category == 'ENTERTAINMENT':
                    amount = random.uniform(200, 2000)
                elif category == 'HEALTHCARE':
                    amount = random.uniform(100, 2000) if random.random() > 0.9 else 0
                elif category == 'EDUCATION':
                    amount = random.uniform(500, 5000) if random.random() > 0.95 else 0
                elif category == 'SHOPPING':
                    amount = random.uniform(200, 3000)
                elif category == 'INVESTMENT':
                    amount = random.uniform(1000, 5000) if day == 5 else 0
                elif category == 'SAVINGS':
                    amount = random.uniform(500, 2000) if day == 1 else 0
                else:
                    amount = random.uniform(100, 1000)
                
                if amount > 0:
                    # Add 2 anomalous transactions
                    is_anomaly = False
                    if category == 'ENTERTAINMENT' and random.random() > 0.98:
                        amount = random.uniform(8000, 15000)  # Anomaly
                        is_anomaly = True
                    
                    expenses.append({
                        'id': expense_id,
                        'user_id': user_id,
                        'category': category,
                        'amount': round(amount, 2),
                        'description': f'{category.title()} expense' + (' (Anomaly)' if is_anomaly else ''),
                        'expense_date': expense_date.strftime('%Y-%m-%d'),
                        'created_at': datetime.now().isoformat()
                    })
                    expense_id += 1
        
        return expenses
    
    def generate_investments(
        self, 
        user_id: int = 1, 
        count: int = 6
    ) -> List[Dict]:
        """
        Generate investment records.
        
        Args:
            user_id: User ID
            count: Number of investments
            
        Returns:
            List of investment records
        """
        investments = []
        
        for i in range(count):
            investment_type = random.choice(self.INVESTMENT_TYPES)
            
            # Amount based on type
            if investment_type == 'STOCKS':
                amount = random.uniform(10000, 50000)
                expected_return = random.uniform(0.10, 0.15)
            elif investment_type == 'MUTUAL_FUNDS':
                amount = random.uniform(5000, 30000)
                expected_return = random.uniform(0.08, 0.12)
            elif investment_type == 'BONDS':
                amount = random.uniform(10000, 40000)
                expected_return = random.uniform(0.05, 0.07)
            elif investment_type == 'CRYPTO':
                amount = random.uniform(2000, 10000)
                expected_return = random.uniform(0.15, 0.30)
            elif investment_type == 'GOLD':
                amount = random.uniform(5000, 20000)
                expected_return = random.uniform(0.06, 0.10)
            else:  # FD
                amount = random.uniform(10000, 50000)
                expected_return = random.uniform(0.06, 0.08)
            
            investment_date = datetime.now() - timedelta(days=random.randint(30, 365))
            
            investments.append({
                'id': i + 1,
                'user_id': user_id,
                'investment_type': investment_type,
                'amount': round(amount, 2),
                'expected_return': round(expected_return, 4),
                'investment_date': investment_date.strftime('%Y-%m-%d'),
                'created_at': datetime.now().isoformat()
            })
        
        return investments
    
    def generate_monthly_summary(
        self, 
        expenses: List[Dict], 
        months: int = 24
    ) -> List[Dict]:
        """
        Generate monthly expense summary.
        
        Args:
            expenses: List of expenses
            months: Number of months
            
        Returns:
            List of monthly summaries
        """
        df = pd.DataFrame(expenses)
        df['expense_date'] = pd.to_datetime(df['expense_date'])
        df['year_month'] = df['expense_date'].dt.to_period('M')
        
        monthly_summary = df.groupby('year_month').agg({
            'amount': 'sum',
            'category': lambda x: x.mode()[0] if not x.mode().empty else 'OTHER'
        }).reset_index()
        
        summary = []
        for _, row in monthly_summary.iterrows():
            summary.append({
                'month': str(row['year_month']),
                'total': round(row['amount'], 2),
                'top_category': row['category']
            })
        
        return summary
    
    def save_to_csv(self, data: List[Dict], filename: str) -> None:
        """Save data to CSV file."""
        if not data:
            return
        
        df = pd.DataFrame(data)
        filepath = os.path.join(os.path.dirname(__file__), filename)
        df.to_csv(filepath, index=False)
        logger.info(f"Saved {len(data)} records to {filepath}")
    
    def generate_all(self) -> Dict:
        """Generate all seed data."""
        logger.info("Generating seed data...")
        
        # Demo user
        user = self.generate_demo_user()
        logger.info(f"Generated demo user: {user['email']}")
        
        # Expenses
        expenses = self.generate_expenses(
            user_id=user['id'],
            months=24,
            monthly_income=user['monthly_income']
        )
        logger.info(f"Generated {len(expenses)} expense records")
        
        # Investments
        investments = self.generate_investments(user_id=user['id'], count=6)
        logger.info(f"Generated {len(investments)} investment records")
        
        # Monthly summary
        monthly_summary = self.generate_monthly_summary(expenses)
        logger.info(f"Generated {len(monthly_summary)} monthly summaries")
        
        return {
            'user': user,
            'expenses': expenses,
            'investments': investments,
            'monthly_summary': monthly_summary
        }
    
    @staticmethod
    def load_real_data_from_db(
        db_url: str,
        min_user_history_days: int = 60,
        limit: int = 10000
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Load real expense and investment data from PostgreSQL database.
        
        Args:
            db_url: PostgreSQL connection URL (e.g., postgresql://user:pass@host:port/db)
            min_user_history_days: Minimum days of history required for users
            limit: Maximum number of expenses to load
            
        Returns:
            Tuple of (expenses list, investments list)
            
        Raises:
            ValueError: If database connection fails or insufficient data
        """
        if not HAS_PSYCOPG2:
            raise ImportError(
                "psycopg2 is required for database operations. "
                "Install it with: pip install psycopg2-binary"
            )
        
        logger.info(f"Loading real data from database: {db_url}")
        
        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor(cursor_factory=DictCursor)
            
            # Get expenses with minimum history
            cutoff_date = datetime.now() - timedelta(days=min_user_history_days)
            
            query = """
            SELECT id, user_id, category, amount, description, expense_date, created_at
            FROM expenses
            WHERE created_at > %s
            ORDER BY expense_date DESC
            LIMIT %s
            """
            
            cursor.execute(query, (cutoff_date, limit))
            expenses_rows = cursor.fetchall()
            
            expenses = [
                {
                    'id': row['id'],
                    'user_id': row['user_id'],
                    'category': row['category'],
                    'amount': float(row['amount']),
                    'description': row['description'] or '',
                    'expense_date': row['expense_date'].isoformat(),
                    'created_at': row['created_at'].isoformat()
                }
                for row in expenses_rows
            ]
            
            logger.info(f"Loaded {len(expenses)} expense records from database")
            
            # Get investments
            query = """
            SELECT id, user_id, investment_type, amount, expected_return, investment_date, created_at
            FROM investments
            ORDER BY investment_date DESC
            """
            
            cursor.execute(query)
            investments_rows = cursor.fetchall()
            
            investments = [
                {
                    'id': row['id'],
                    'user_id': row['user_id'],
                    'investment_type': row['investment_type'],
                    'amount': float(row['amount']),
                    'expected_return': float(row['expected_return']) if row['expected_return'] else 0.0,
                    'investment_date': row['investment_date'].isoformat(),
                    'created_at': row['created_at'].isoformat()
                }
                for row in investments_rows
            ]
            
            logger.info(f"Loaded {len(investments)} investment records from database")
            
            cursor.close()
            conn.close()
            
            if not expenses:
                raise ValueError(
                    f"No expense data found. Ensure users have history greater than {min_user_history_days} days"
                )
            
            return expenses, investments
            
        except psycopg2.OperationalError as e:
            logger.error(f"Failed to connect to database: {e}")
            raise ValueError(f"Database connection failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading real data from database: {e}")
            raise


def main():
    """Main function to generate seed data."""
    generator = SeedDataGenerator(seed=42)
    
    data = generator.generate_all()
    
    # Save to CSV files for reference
    generator.save_to_csv(data['expenses'], 'demo_expenses.csv')
    generator.save_to_csv(data['investments'], 'demo_investments.csv')
    
    logger.info("=" * 60)
    logger.info("Seed data generation complete!")
    logger.info("=" * 60)
    logger.info(f"Demo User: {data['user']['email']} / {data['user']['password']}")
    logger.info(f"Monthly Income: ₹{data['user']['monthly_income']:,.0f}")
    logger.info(f"Total Expenses: {len(data['expenses'])}")
    logger.info(f"Total Investments: {len(data['investments'])}")
    
    # Print sample data
    logger.info("\nSample Expenses:")
    for exp in data['expenses'][:5]:
        logger.info(f"  {exp['expense_date']}: {exp['category']} - ₹{exp['amount']:,.2f}")
    
    logger.info("\nSample Investments:")
    for inv in data['investments']:
        logger.info(f"  {inv['investment_type']}: ₹{inv['amount']:,.2f} ({inv['expected_return']:.1%} expected)")
    
    return data


if __name__ == "__main__":
    main()
