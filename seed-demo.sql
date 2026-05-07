-- FinGuard AI - Demo Data Seed Script
-- Run this after the backend has created the tables

-- Insert demo user (password is BCrypt hash of "Demo@123")
INSERT INTO users (id, name, email, password, monthly_income, created_at, updated_at)
VALUES (
    1,
    'Demo User',
    'demo@finguard.ai',
    '$2a$10$xQKJ9qZ5fZ5fZ5fZ5fZ5fOeKqZ5fZ5fZ5fZ5fZ5fZ5fZ5fZ5fZ5fZ',
    50000.00,
    NOW(),
    NOW()
)
ON CONFLICT (email) DO NOTHING;

-- Reset sequence
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- Insert sample expenses for the last 3 months
INSERT INTO expenses (user_id, category, amount, description, expense_date, created_at)
SELECT 
    1,
    category,
    amount,
    description,
    expense_date,
    NOW()
FROM (
    -- Month 1 expenses
    SELECT 'FOOD' as category, 250.00 as amount, 'Grocery shopping' as description, CURRENT_DATE - INTERVAL '60 days' as expense_date UNION ALL
    SELECT 'FOOD', 180.00, 'Restaurant', CURRENT_DATE - INTERVAL '58 days' UNION ALL
    SELECT 'TRANSPORT', 500.00, 'Fuel', CURRENT_DATE - INTERVAL '57 days' UNION ALL
    SELECT 'BILLS', 2500.00, 'Electricity bill', CURRENT_DATE - INTERVAL '55 days' UNION ALL
    SELECT 'ENTERTAINMENT', 800.00, 'Movie tickets', CURRENT_DATE - INTERVAL '54 days' UNION ALL
    SELECT 'SHOPPING', 1500.00, 'Clothing', CURRENT_DATE - INTERVAL '52 days' UNION ALL
    SELECT 'FOOD', 300.00, 'Grocery shopping', CURRENT_DATE - INTERVAL '50 days' UNION ALL
    SELECT 'HEALTHCARE', 1200.00, 'Medical checkup', CURRENT_DATE - INTERVAL '48 days' UNION ALL
    
    -- Month 2 expenses
    SELECT 'FOOD', 280.00, 'Grocery shopping', CURRENT_DATE - INTERVAL '30 days' UNION ALL
    SELECT 'FOOD', 220.00, 'Restaurant', CURRENT_DATE - INTERVAL '28 days' UNION ALL
    SELECT 'TRANSPORT', 550.00, 'Fuel', CURRENT_DATE - INTERVAL '27 days' UNION ALL
    SELECT 'BILLS', 2800.00, 'Electricity + Water', CURRENT_DATE - INTERVAL '25 days' UNION ALL
    SELECT 'ENTERTAINMENT', 1200.00, 'Concert tickets', CURRENT_DATE - INTERVAL '24 days' UNION ALL
    SELECT 'SHOPPING', 2000.00, 'Electronics', CURRENT_DATE - INTERVAL '22 days' UNION ALL
    SELECT 'FOOD', 320.00, 'Grocery shopping', CURRENT_DATE - INTERVAL '20 days' UNION ALL
    SELECT 'INVESTMENT', 5000.00, 'Mutual fund SIP', CURRENT_DATE - INTERVAL '18 days' UNION ALL
    
    -- Month 3 (current) expenses
    SELECT 'FOOD', 300.00, 'Grocery shopping', CURRENT_DATE - INTERVAL '10 days' UNION ALL
    SELECT 'FOOD', 250.00, 'Restaurant', CURRENT_DATE - INTERVAL '8 days' UNION ALL
    SELECT 'TRANSPORT', 600.00, 'Fuel', CURRENT_DATE - INTERVAL '7 days' UNION ALL
    SELECT 'BILLS', 3000.00, 'Rent', CURRENT_DATE - INTERVAL '5 days' UNION ALL
    SELECT 'ENTERTAINMENT', 15000.00, 'Vacation (ANOMALY)', CURRENT_DATE - INTERVAL '4 days' UNION ALL
    SELECT 'SHOPPING', 1800.00, 'Groceries', CURRENT_DATE - INTERVAL '3 days' UNION ALL
    SELECT 'FOOD', 350.00, 'Grocery shopping', CURRENT_DATE - INTERVAL '2 days' UNION ALL
    SELECT 'SAVINGS', 2000.00, 'Emergency fund', CURRENT_DATE - INTERVAL '1 day'
) AS sample_data;

-- Insert sample investments
INSERT INTO investments (user_id, investment_type, amount, expected_return, investment_date, created_at)
VALUES
    (1, 'STOCKS', 25000.00, 0.12, CURRENT_DATE - INTERVAL '180 days', NOW()),
    (1, 'MUTUAL_FUNDS', 15000.00, 0.10, CURRENT_DATE - INTERVAL '150 days', NOW()),
    (1, 'BONDS', 30000.00, 0.07, CURRENT_DATE - INTERVAL '120 days', NOW()),
    (1, 'GOLD', 10000.00, 0.08, CURRENT_DATE - INTERVAL '90 days', NOW()),
    (1, 'FD', 40000.00, 0.065, CURRENT_DATE - INTERVAL '60 days', NOW()),
    (1, 'CRYPTO', 5000.00, 0.20, CURRENT_DATE - INTERVAL '30 days', NOW())
ON CONFLICT DO NOTHING;

-- Verify data
SELECT 'Users created:' as info, COUNT(*) as count FROM users WHERE email = 'demo@finguard.ai'
UNION ALL
SELECT 'Expenses created:', COUNT(*) FROM expenses WHERE user_id = 1
UNION ALL
SELECT 'Investments created:', COUNT(*) FROM investments WHERE user_id = 1;
