@echo off
REM Activates the Python virtual environment and runs the main script

REM Navigate to the project directory
cd /d "C:\path\to\soul_symphony"  REM Replace with the actual path to your project

REM Activate the virtual environment
call .\venv\Scripts\activate.bat  REM Ensure this matches the correct venv path

REM Run the main Python script
python main.py

REM Pause the terminal to see output before closing
pause
