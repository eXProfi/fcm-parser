@echo off
:: Activate virtual environment
call venv\Scripts\activate.bat

:: Launch app
python gradio_app.py

:: Deactivate virtualenv after closing app
call venv\Scripts\deactivate.bat
