# Senti-Nalysis 🎭

A modern **Streamlit web application** for sentiment analysis labeling. Select from pre-loaded CSV files, label sentiments, and download comprehensive reports with automatic backend storage.

## Features ✨

- **Streamlit Interface**: Fast, interactive, and modern UI built with Streamlit
- **File Selection**: Choose from pre-loaded CSV files in the documents folder
- **Interactive Labeling**: Label each text entry with positive, neutral, or negative sentiment
- **Progress Tracking**: Real-time progress bar showing completion status
- **Session State Management**: Built-in progress tracking with Streamlit session state
- **Completion Tracking**: Completed files are marked and tracked to prevent duplicate work
- **Backend Storage**: Completed reports are automatically saved to the results folder
- **Report Generation**: Download labeled data as a CSV file
- **Beautiful UI**: Modern, responsive design with custom styling and gradients
- **No Separate Server Needed**: All-in-one Streamlit application

## File Requirements 📋

Your CSV file should contain the following columns:
- `user`: Username or identifier
- `text`: The text content to be labeled

Optional columns (will be ignored if present):
- `sentiment`: Original sentiment (for reference)
- `score`: Sentiment score (for reference)

## Setup & Installation 🛠️

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   This installs Streamlit and pandas for the application.

2. **Start the Application**
   
   **On macOS/Linux:**
   ```bash
   chmod +x start_streamlit.sh
   ./start_streamlit.sh
   ```
   Or manually:
   ```bash
   streamlit run streamlit_app.py
   ```
   
   **On Windows:**
   ```batch
   start_streamlit.bat
   ```
   Or manually:
   ```batch
   streamlit run streamlit_app.py
   ```

3. **Access the Application**
   - The app will automatically open in your browser at: `http://localhost:8501`
   - If it doesn't open automatically, navigate to: `http://localhost:8501`

## How to Use 🚀

1. **Resume or Start New**
   - If you have saved progress, you'll see a resume screen
   - Click "📂 Resume Session" to continue where you left off
   - Or click "🆕 Start New Session" to begin fresh

2. **Select a CSV File**
   - Choose from the dropdown list of available files in the documents folder
   - Completed files will be marked with ✅ and cannot be selected
   - Click "🔄 Reset Completed Files" if you need to re-label completed files

3. **Enter Your Name**
   - Enter your name when prompted
   - This will be used in the report filename

4. **Start Labeling**
   - Click "🚀 Start Labeling" to begin
   - Read each text entry carefully
   - Select the appropriate sentiment:
     - 😊 **Positive** - Expresses positive emotion or satisfaction
     - 😐 **Neutral** - Neither positive nor negative
     - 😞 **Negative** - Expresses negative emotion or dissatisfaction
   - Click "✅ Submit & Next" to move to the next entry

5. **Save & Resume (Optional)**
   - Click "💾 Save & Exit" in the sidebar at any time
   - Your progress is saved to disk and persists across sessions
   - Next time you open the app, you can resume from where you left off

6. **Track Your Progress**
   - View real-time progress in the sidebar
   - See progress bar showing completion percentage
   - Current record number is displayed at the top

7. **Download Report**
   - Once all entries are labeled, you'll see a completion screen
   - View summary statistics (Total, Positive, Neutral, Negative)
   - Click "📥 Download Report" to save your labeled data
   - The report will be:
     - Downloaded to your computer
     - Automatically saved to the `./results` folder with format: `{username}_{filename}-{timestamp}.csv`
   - The file will be marked as completed

8. **Start New Session**
   - Click "🔄 Start New Session" to label another file
   - Select a different file and repeat the process

## Technologies Used 💻

### Framework
- **Streamlit** - Modern Python web framework for data applications
- **Pandas** - Data manipulation and CSV handling
- **Python 3.8+** - Core programming language

### Features
- Built-in session state management
- Real-time UI updates
- Native CSV download functionality
- Custom HTML/CSS styling with `st.markdown()`

## File Structure 📁

```
Senti-Nalysis/v.3.0.0/
├── streamlit_app.py        # Main Streamlit application
├── requirements.txt        # Python dependencies
├── start_streamlit.sh      # Startup script (macOS/Linux)
├── start_streamlit.bat     # Startup script (Windows)
├── README.md               # This file
├── QUICK_START.md          # Quick start guide
├── GET_STARTED.md          # Quick overview
├── MIGRATION_GUIDE.md      # Flask to Streamlit migration details
├── SAVE_RESUME_GUIDE.md    # Save & Resume feature guide
├── TESTING.md              # Testing procedures
├── DEPLOYMENT.md           # Deployment guide
├── CHANGELOG.md            # Version history
├── CONVERSION_SUMMARY.md   # Conversion overview
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── documents/              # Source CSV files (22 files)
│   ├── Tutor room A_Charity.csv
│   ├── Tutor room B_Charity.csv
│   └── ... (20 more files)
├── results/                # Completed reports saved here
├── images/
│   ├── Senti-Nalysis_icon.png
│   └── Senti-Nalysis_logo.png
├── .completed_files.txt    # Tracks completed files (auto-generated)
├── .progress/              # Progress storage (auto-generated)
│   └── current_session.json
└── sample_data.csv         # Sample data for reference
```

## Browser Compatibility 🌐

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

Streamlit apps are responsive and work on desktop, tablet, and mobile devices.

## Backend Storage 📦

When a user completes labeling and downloads their report:

1. **User Download**: The CSV file is downloaded to the user's computer via Streamlit's download button
2. **Server Storage**: A copy is automatically saved to `./results/` with the format:
   ```
   {username}_{filename}-{timestamp}.csv
   ```
   Example: `John_Doe_Tutor room A_Charity-20231103_143022.csv`

3. **Access Backend Files**: All completed reports are stored in the `./results/` directory for backend access and analysis

## Important Notes 📝

- **Session State**: Active session data uses Streamlit's session state
- **Save & Resume**: Progress is saved to `.progress/current_session.json` for persistent storage
- **Completion Tracking**: File completion status is stored in `.completed_files.txt`
- **CSV Parsing**: Pandas handles CSV parsing with support for all standard formats
- **Proper Escaping**: Reports are generated with proper CSV escaping via pandas
- **Real-time Updates**: UI updates instantly as you interact with the application
- **No Database Required**: All data is file-based for simplicity

## Sample Data 🧪

A sample CSV file (`sample_data.csv`) is included with 10 sample entries for testing the application.

## Troubleshooting 🔧

### Port Already in Use
If port 8501 is already in use, you can specify a different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Streamlit Not Found
Make sure you've installed the dependencies:
```bash
pip install -r requirements.txt
```

### Results Directory
The results directory is automatically created when needed. If you don't see it, check file permissions.

### Completed Files Tracking
If you need to manually reset completed files, delete the `.completed_files.txt` file:
```bash
rm .completed_files.txt
```

### App Not Loading
Try clearing Streamlit cache:
```bash
streamlit cache clear
```

### Module Import Errors
Make sure you're using Python 3.8 or higher:
```bash
python --version
```

---

Made with ❤️ for sentiment analysis research

