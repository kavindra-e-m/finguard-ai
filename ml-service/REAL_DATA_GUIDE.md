# Using Real Data for ML Model Training

This guide explains how to transition your FinGuard AI ML models from synthetic to real data.

## Prerequisites

1. **PostgreSQL Database**: Ensure your backend database is running with the FinGuard schema
2. **User Data**: Your database must have real user transactions (expenses and investments)
3. **Python Dependencies**: Install `psycopg2-binary` for database connectivity

```bash
pip install psycopg2-binary
```

## Step 1: Prepare Your Database

Ensure your PostgreSQL database is populated with real user data:

```sql
-- Verify expenses table has data
SELECT COUNT(*) FROM expenses;

-- Verify investments table has data
SELECT COUNT(*) FROM investments;

-- Check for users with sufficient history (recommended: 60+ days)
SELECT user_id, COUNT(*) as transaction_count, 
       MAX(expense_date) - MIN(expense_date) as date_range
FROM expenses
GROUP BY user_id
HAVING COUNT(*) >= 10
ORDER BY transaction_count DESC;
```

## Step 2: Set Up Database Connection

### Option A: Environment Variable

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://finguard_user:finguard_pass@localhost:5432/finguard_db"

# Or on Windows (PowerShell):
$env:DATABASE_URL="postgresql://finguard_user:finguard_pass@localhost:5432/finguard_db"
```

### Option B: Create .env File

Create a `.env` file in the `ml-service` directory:

```env
DATABASE_URL=postgresql://finguard_user:finguard_pass@localhost:5432/finguard_db
DEBUG=false
LOG_LEVEL=INFO
```

## Step 3: Train Models with Real Data

### Basic Usage (Default Settings)

```bash
cd ml-service
python ml/train_all_models.py --use-real-data
```

### Specify Database URL Directly

```bash
python ml/train_all_models.py --use-real-data --db-url "postgresql://username:password@localhost:5432/finguard_db"
```

### Train with Synthetic Data (Default)

```bash
python ml/train_all_models.py
```

## Step 4: Verify Model Training

After training, check the output logs:

```
============================================================
Training Personality Detector
Using REAL DATA from database
============================================================

Loaded 5000 expense records from database
Loaded 250 investment records from database
Extracted 42 personality feature vectors from 42 unique users
```

Models are saved to: `ml-service/models/`

## What Gets Trained on Real Data

### 1. **Personality Detector**
Trained on features extracted from your users' actual expense patterns:
- Savings ratio (from real expenses)
- Expense variability (from transaction history)
- Investment frequency (from actual investments)
- Risk exposure (from investment types)
- Category spending ratios (food, entertainment, etc.)

### 2. **Stress Predictor**
Learns from real financial behavior:
- Debt-to-income ratios
- Actual savings rates
- Expense growth trends
- Income stability
- Emergency fund coverage

### 3. **Anomaly Detector**
Trained on your actual transaction patterns:
- Real transaction amounts
- Actual spending patterns by day/month
- Category-specific behaviors
- Detects unusual transactions specific to your users

## Data Requirements for Accurate Training

| Model | Minimum Data | Recommended |
|-------|-------------|-------------|
| **Personality Detector** | 10+ users, 100+ transactions each | 50+ users, 500+ transactions |
| **Stress Predictor** | 10+ users, 100+ transactions each | 50+ users, 500+ transactions |
| **Anomaly Detector** | 100+ transactions | 1000+ transactions |

## Monitoring Training Progress

The training script provides detailed logs:

```bash
# View logs with timestamps
python ml/train_all_models.py --use-real-data 2>&1 | tee training.log

# Monitor specific user processing
python ml/train_all_models.py --use-real-data 2>&1 | grep "User"
```

## Fallback Behavior

If real data loading fails, the training automatically falls back to synthetic data:

```
ERROR: Failed to load real data: Connection refused
WARNING: Falling back to synthetic data.
```

## Troubleshooting

### Connection Refused

```
psycopg2.OperationalError: could not connect to server
```

**Solution**: Verify PostgreSQL is running and credentials are correct

```bash
# Test connection
psql -h localhost -U finguard_user -d finguard_db -c "SELECT 1"
```

### No Data Extracted

```
ERROR: No valid features extracted from real data
```

**Solutions**:
1. Ensure users have at least 10 transactions
2. Check that `category` field is populated in expenses
3. Verify `investment_type` is set in investments table

```sql
-- Check for missing categories
SELECT COUNT(*) FROM expenses WHERE category IS NULL;

-- Check for users with insufficient history
SELECT user_id, COUNT(*) FROM expenses GROUP BY user_id HAVING COUNT(*) < 10;
```

### psycopg2 Not Found

```
ImportError: No module named 'psycopg2'
```

**Solution**: Install the package

```bash
pip install psycopg2-binary
```

## Advanced Configuration

### Filter by Date Range

Modify `ml/train_all_models.py` to limit training data:

```python
expenses, investments = SeedDataGenerator.load_real_data_from_db(
    db_url,
    min_user_history_days=90,  # At least 90 days of history
    limit=50000  # Load up to 50,000 expenses
)
```

### Custom Feature Extraction

Extend feature engineering in `ml/utils/feature_engineering.py`:

```python
# Add custom features
def extract_custom_features(expenses_df):
    # Your custom feature logic
    return features
```

### Scheduled Retraining

Set up a cron job to retrain models with fresh data:

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/finguard-ai/ml-service && python ml/train_all_models.py --use-real-data
```

## Comparing Real vs Synthetic Data

### Synthetic Data
- ✅ Consistent, reproducible results
- ✅ No privacy concerns
- ✅ Fast training
- ❌ May not capture real user patterns
- ❌ May overfit to artificial distributions

### Real Data
- ✅ Captures actual user behavior
- ✅ More accurate predictions
- ✅ Better generalization
- ❌ Requires data privacy compliance
- ❌ Quality depends on data completeness

## Data Privacy Considerations

When using real user data:

1. **Ensure GDPR/Data Protection Compliance**: Follow applicable regulations
2. **Data Anonymization**: Consider anonymizing sensitive information before training
3. **Access Control**: Restrict database access to authorized personnel only
4. **Audit Logging**: Log all data access for compliance

## Performance Baseline

Expected training times on standard hardware:

| Scenario | Time | Data Size |
|----------|------|-----------|
| Synthetic (2000 samples) | ~5 min | 6 MB |
| Real (5000 expenses) | ~10 min | 50 MB |
| Real (50000 expenses) | ~30 min | 500 MB |

## Model Performance Metrics

After training with real data, models are evaluated on:

- **Personality Detector**: Precision, Recall, F1-score per class
- **Stress Predictor**: Accuracy, AUC-ROC for stress levels
- **Anomaly Detector**: Detection rate, false positive rate

Check logs for detailed metrics after training completes.

## Next Steps

1. Train models with real data: `python ml/train_all_models.py --use-real-data`
2. Verify model accuracy on your specific use case
3. Deploy trained models to production
4. Set up scheduled retraining with new data monthly/quarterly

For additional support, check the main README or backend documentation.
