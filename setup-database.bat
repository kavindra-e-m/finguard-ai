@echo off
echo ========================================
echo PostgreSQL Database Setup
echo ========================================
echo.

echo Creating database and user...
echo.

psql -U postgres -c "CREATE DATABASE finguard_db;"
psql -U postgres -c "CREATE USER finguard_user WITH PASSWORD 'K@VICLOWn17';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE finguard_db TO finguard_user;"
psql -U postgres -d finguard_db -c "GRANT ALL ON SCHEMA public TO finguard_user;"

echo.
echo ========================================
echo Database setup complete!
echo ========================================
echo.
pause
