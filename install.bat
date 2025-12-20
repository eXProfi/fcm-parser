@echo off
:: Create virtualenv
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip install gradio


:: Launch app 
python gradio_app.py

:: Deactivate virtualenv after closing app
venv\Scripts\deactivate.bat