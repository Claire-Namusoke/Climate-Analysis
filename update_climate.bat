@echo off
REM Climate Data Auto-Update Script
REM This batch file updates climate data from the World Bank API

echo ================================================
echo Climate Data Auto-Update
echo ================================================
echo.

REM Navigate to the script directory
cd /d "%~dp0"

REM Run the scheduler with the virtual environment Python
.venv\Scripts\python.exe scheduler.py

REM Check if update was successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================
    echo Update completed successfully!
    echo ================================================
) else (
    echo.
    echo ================================================
    echo Update failed! Check error messages above.
    echo ================================================
)

REM Uncomment the line below if you want the window to stay open
REM pause
