@echo off
echo ========================================
echo Starting FinGuard AI ML Service
echo ========================================
cd ml-service
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
