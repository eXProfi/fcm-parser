@echo off
setlocal enabledelayedexpansion

:: Ensure Python 3.11.9 is available
set "PY_CMD=py -3.11"
%PY_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.11.9 is required. Please install it from https://www.python.org/downloads/release/python-3119/
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('%PY_CMD% --version') do set "PY_VERSION=%%v"
if not "!PY_VERSION!"=="3.11.9" (
    echo Found Python !PY_VERSION!, but Python 3.11.9 is required.
    exit /b 1
)

:: Create virtualenv with Python 3.11.9
%PY_CMD% -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment with Python 3.11.9.
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

for /f "tokens=2 delims= " %%v in ('python --version') do set "VENV_PY_VERSION=%%v"
if not "!VENV_PY_VERSION!"=="3.11.9" (
    echo Virtual environment is not using Python 3.11.9.
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install gradio

:: Launch app 
python gradio_app.py

:: Deactivate virtualenv after closing app
call venv\Scripts\deactivate.bat
