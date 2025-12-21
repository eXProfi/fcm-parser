@echo off
setlocal enabledelayedexpansion

set "PY_VERSION=3.11.9"
set "PY_DOWNLOAD_URL=https://www.python.org/ftp/python/%PY_VERSION%/python-%PY_VERSION%-amd64.exe"
set "PY_INSTALLER=%TEMP%\python-%PY_VERSION%-amd64.exe"
set "PY_INSTALL_DIR=%~dp0python311"
set "PY_EMBEDDED_EXE=%PY_INSTALL_DIR%\python.exe"
set "PY_CMD_QUOTED="

:: Try to use an existing Python 3.11.9 installation
for /f "tokens=2 delims= " %%v in ('py -3.11 --version 2^>nul') do (
    if "%%v"=="%PY_VERSION%" (
        set "PY_CMD_QUOTED=py -3.11"
    )
)

:: Fallback to a bundled installation in the project folder
if not defined PY_CMD_QUOTED (
    if exist "%PY_EMBEDDED_EXE%" (
        for /f "tokens=2 delims= " %%v in ('"%PY_EMBEDDED_EXE%" --version 2^>nul') do (
            if "%%v"=="%PY_VERSION%" (
                set "PY_CMD_QUOTED=\"%PY_EMBEDDED_EXE%\""
            )
        )
    )
)

:: Download and install Python locally if it is missing
if not defined PY_CMD_QUOTED (
    echo Downloading Python %PY_VERSION%...
    powershell -Command "Invoke-WebRequest -Uri '%PY_DOWNLOAD_URL%' -OutFile '%PY_INSTALLER%'" || (
        echo Failed to download Python installer.
        exit /b 1
    )

    echo Installing Python %PY_VERSION% into %PY_INSTALL_DIR%...
    "%PY_INSTALLER%" /quiet InstallAllUsers=0 TargetDir="%PY_INSTALL_DIR%" Include_pip=1 Include_test=0 PrependPath=0 || (
        echo Failed to install Python.
        exit /b 1
    )

    if not exist "%PY_EMBEDDED_EXE%" (
        echo Python executable was not created at %PY_EMBEDDED_EXE%.
        exit /b 1
    )

    set "PY_CMD_QUOTED=\"%PY_EMBEDDED_EXE%\""
)

echo Using Python command: %PY_CMD_QUOTED%

:: Create virtualenv with Python 3.11.9
call %PY_CMD_QUOTED% -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment with Python %PY_VERSION%.
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

for /f "tokens=2 delims= " %%v in ('python --version') do set "VENV_PY_VERSION=%%v"
if not "!VENV_PY_VERSION!"=="%PY_VERSION%" (
    echo Virtual environment is not using Python %PY_VERSION%.
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install gradio

:: Launch app 
python gradio_app.py

:: Deactivate virtualenv after closing app
call venv\Scripts\deactivate.bat
