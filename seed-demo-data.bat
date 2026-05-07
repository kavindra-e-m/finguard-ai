@echo off
echo ========================================
echo Seeding Demo Data to Database
echo ========================================
cd ml-service
python data\seed_data.py
pause
