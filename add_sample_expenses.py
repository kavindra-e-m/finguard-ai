import requests
from datetime import datetime, timedelta
import random

# Configuration
API_URL = "http://localhost:8081/api"
EMAIL = "kishore@gmail.com"
PASSWORD = "123546"

# Categories and typical amounts
EXPENSE_DATA = [
    ("FOOD", 50, 200),
    ("TRANSPORT", 20, 100),
    ("UTILITIES", 100, 300),
    ("ENTERTAINMENT", 30, 150),
    ("HEALTHCARE", 50, 500),
    ("SHOPPING", 100, 400),
    ("EDUCATION", 200, 1000),
    ("OTHER", 20, 200),
]

def login():
    response = requests.post(f"{API_URL}/auth/login", json={
        "email": EMAIL,
        "password": PASSWORD
    })
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"Login failed: {response.text}")
        return None

def add_expenses(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    # Generate expenses for last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    expenses_added = 0
    current_date = start_date
    
    while current_date <= end_date:
        # Add 5-10 random expenses per month
        num_expenses = random.randint(5, 10)
        
        for _ in range(num_expenses):
            category, min_amt, max_amt = random.choice(EXPENSE_DATA)
            amount = round(random.uniform(min_amt, max_amt), 2)
            
            expense_date = current_date + timedelta(days=random.randint(0, 28))
            
            expense = {
                "category": category,
                "amount": amount,
                "description": f"{category.lower()} expense",
                "expenseDate": expense_date.strftime("%Y-%m-%d")
            }
            
            response = requests.post(f"{API_URL}/expenses", json=expense, headers=headers)
            if response.status_code == 200:
                expenses_added += 1
            else:
                print(f"Failed to add expense: {response.text}")
        
        # Move to next month
        current_date = current_date + timedelta(days=30)
    
    print(f"✅ Successfully added {expenses_added} expenses!")

if __name__ == "__main__":
    print("🔐 Logging in...")
    token = login()
    
    if token:
        print("📊 Adding sample expenses...")
        add_expenses(token)
        print("✨ Done! Refresh your dashboard to see predictions.")
    else:
        print("❌ Failed to login. Check credentials.")
