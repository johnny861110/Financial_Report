@echo off
REM 傳入參數：股票代號、年度
set STOCK_ID=2337
set ROC_YEAR=114

venv\Scripts\python.exe twse_scraper.py %STOCK_ID% %ROC_YEAR%
pause
