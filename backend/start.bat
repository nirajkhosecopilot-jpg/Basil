@echo off
REM Startup script for backend with virtual environment support

echo Starting Basil Backend...

REM Check if virtual environment exists
if exist "%~dp0venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%~dp0venv\Scripts\activate.bat"
) else if exist "%~dp0.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%~dp0.venv\Scripts\activate.bat"
) else (
    echo WARNING: No virtual environment found. Using system Python.
    echo Please create a virtual environment:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
)

REM Run uvicorn
echo Running uvicorn...
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
