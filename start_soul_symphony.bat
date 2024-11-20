@echo off
cd /d "C:\path\to\soul_symphony"   REM Change this to the path where your project is located
call venv\Scripts\activate.bat    REM Adjust this path if your venv is located elsewhere
python main.py
pause
