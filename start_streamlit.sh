#!/bin/bash
# Start script for Senti-Nalysis Streamlit App (macOS/Linux)

echo "================================================"
echo "  Starting Senti-Nalysis Streamlit App..."
echo "================================================"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit is not installed. Installing dependencies..."
    pip install -r requirements.txt
fi

echo "Starting Streamlit server..."
echo "The app will open in your default browser."
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo ""

# Start Streamlit app
streamlit run streamlit_app.py

