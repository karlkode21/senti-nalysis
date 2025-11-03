# Quick Start Guide - Senti-Nalysis 🚀

## Current Status ✅
Your Streamlit app is ready to run! Access it at **http://localhost:8501**

## What's New? 🎉

### Streamlit Web Application
- Modern, interactive interface built with Streamlit
- Real-time updates and progress tracking
- Built-in session state management
- No separate backend server needed!

### Backend File Storage
- When users complete a file and download their report, a copy is **automatically saved** to `./results/`
- Filename format: `{username}_{filename}-{timestamp}.csv`
- Example: `John_Doe_Tutor room A_Charity-20231103_143022.csv`

### File Access
- **User**: Downloads the CSV file to their computer
- **You (Backend)**: Access completed files in `./results/` directory

## How to Start the Application

### Option 1: Using the Startup Script (Easiest)

**macOS/Linux:**
```bash
chmod +x start_streamlit.sh
./start_streamlit.sh
```

**Windows:**
```cmd
start_streamlit.bat
```

### Option 2: Manual Start
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Start the Streamlit app
streamlit run streamlit_app.py
```

## Accessing the Application

1. **The app will automatically open** in your default browser at: http://localhost:8501
2. If it doesn't open automatically, go to: http://localhost:8501
3. Users will see the file selection interface
4. They select a file, enter their name, and start labeling
5. When complete, the report is:
   - Downloaded to their computer
   - Saved to your `./results/` folder

## Checking Backend Files

View completed reports:
```bash
ls -lh results/
```

View a specific report:
```bash
cat results/John_Doe_Tutor_room_A_Charity-20231103_143022.csv
```

## Streamlit Features

The Streamlit app provides:

- 📊 **Interactive UI** - Modern, responsive design
- 💾 **Save & Resume** - Persistent progress across sessions
- 📥 **Download Button** - Built-in CSV download functionality
- 📈 **Progress Bar** - Real-time labeling progress
- 🎨 **Custom Styling** - Beautiful gradient headers and cards
- 🔄 **Auto-Refresh** - Smooth transitions between screens
- 📂 **File-based Storage** - Progress saved to `.progress/` directory

## Stopping the Application

Press `Ctrl+C` in the terminal where the app is running.

## File Naming Convention

The backend automatically generates filenames using:
```
{username}_{filename}-{timestamp}.csv
```

Where:
- `username`: User's name with spaces replaced by underscores
- `filename`: Original CSV filename without .csv extension
- `timestamp`: Format YYYYMMDD_HHMMSS

### Examples:
- `Sarah_Johnson_Tutor room B_Warner-20231103_094522.csv`
- `Mike_Chen_Tutor room L_Charity-20231103_153045.csv`

## Features Summary

✅ File selection from documents folder (22 CSV files)
✅ Save & Resume progress
✅ Completion tracking with visual indicators
✅ Automatic backend storage
✅ User download
✅ Reset completed files option

## Need Help?

Check the full README.md for detailed documentation and troubleshooting.

---

**Application URL**: http://localhost:8501
**Results Directory**: `./results/`
**Documents Directory**: `./documents/`

