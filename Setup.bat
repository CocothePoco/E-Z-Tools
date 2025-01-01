@echo off
echo [92m=== E-Z Tools Setup ===[0m
echo.
python --version > nul 2>&1
if errorlevel 1 (
    echo [91mError: Python is not installed or not in PATH[0m
    echo Please install Python 3.8 or newer from https://python.org
    pause
    exit /b 1
)
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)
call venv\Scripts\activate
echo Upgrading pip...
python -m pip install --upgrade pip
echo Installing required packages...
pip install gradio requests
if not exist ".env" (
    echo Creating .env file...
    echo API_KEY=your_api_key_here > .env
)
echo.
echo [92mSetup completed successfully![0m
echo.
echo To start E-Z Tools:
echo 1. Run 'venv\Scripts\activate' to activate the virtual environment
echo 2. Run 'python script.py' to start the application
echo.
pause
