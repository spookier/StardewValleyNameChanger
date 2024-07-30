@echo off
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed or not in the system PATH.
    echo Please install Python and add it to your system PATH.
    pause
    exit /b
)
python "%~dp0script.py"
pause