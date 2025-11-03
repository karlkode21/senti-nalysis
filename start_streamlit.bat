@echo off
REM Start script for Senti-Nalysis Streamlit App (Windows)

echo ================================================
echo   Starting Senti-Nalysis Streamlit App...
echo ================================================
echo.

REM Check if streamlit is installed
where streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit is not installed. Installing dependencies...
    pip install -r requirements.txt
)

echo Starting Streamlit server...
echo The app will open in your default browser.
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

REM Start Streamlit app
streamlit run streamlit_app.py

