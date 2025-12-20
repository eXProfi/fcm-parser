@echo off
:: Activate virtual environment
cd .. && call venv\Scripts\activate.bat

:: Launch app
python fcm-parser\gradio_app.py

:: Deactivate virtualenv after closing app
venv\Scripts\deactivate.bat
