@echo off
cd C:\Users\tonib\Desktop\TradingBot
start "" uvicorn server:app --reload
timeout /t 3
cd trading-dashboard
start "" npm start
timeout /t 5
start "" chrome http://localhost:3000
exit