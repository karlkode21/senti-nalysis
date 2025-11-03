# Migration Guide: Flask to Streamlit 🔄

This document explains the conversion from the Flask-based web app to the Streamlit application.

## What Changed? 🔄

### Technology Stack

**Before (Flask):**
- Frontend: HTML, CSS, JavaScript
- Backend: Flask + Flask-CORS
- State Management: localStorage (browser)
- File Serving: Static file server
- Port: 5001

**After (Streamlit):**
- Framework: Streamlit (Python-only)
- State Management: Streamlit session state
- File Handling: Built-in pandas + Streamlit
- Port: 8501

## Key Improvements ✨

### 1. **Simplified Architecture**
- **Before**: Separate HTML/CSS/JS files + Python backend
- **After**: Single Python file with all logic and UI

### 2. **No Client-Server Communication**
- **Before**: JavaScript makes API calls to Flask backend
- **After**: All processing happens server-side with instant UI updates

### 3. **Better State Management**
- **Before**: localStorage for browser-based persistence
- **After**: Streamlit session state (per-session, server-side)

### 4. **Native Components**
- **Before**: Custom HTML forms and buttons
- **After**: Built-in Streamlit widgets (selectbox, buttons, progress bars)

### 5. **Easier Maintenance**
- **Before**: Maintain HTML, CSS, JS, and Python separately
- **After**: Single Python file with embedded styling

## Feature Parity ✅

All features from the Flask version are preserved:

| Feature | Flask Version | Streamlit Version |
|---------|---------------|-------------------|
| File Selection | ✅ Dropdown | ✅ st.selectbox |
| Username Input | ✅ Text Input | ✅ st.text_input |
| Progress Bar | ✅ CSS + JS | ✅ st.progress |
| Sentiment Selection | ✅ Radio Buttons | ✅ Buttons |
| Save & Exit | ✅ localStorage | ⚠️ Session-based |
| Download CSV | ✅ Blob + Link | ✅ st.download_button |
| Backend Storage | ✅ API Call | ✅ Direct File Write |
| Completion Tracking | ✅ localStorage | ✅ File-based (.completed_files.txt) |
| Resume Session | ✅ localStorage | ⚠️ Not available* |

*Note: Streamlit uses session state which is cleared when the browser tab is closed. To add persistent "Save & Resume", you would need to implement file-based progress tracking similar to completion tracking.

## File Changes 📝

### New Files
- `streamlit_app.py` - Main Streamlit application
- `start_streamlit.sh` - Streamlit startup script (Unix)
- `start_streamlit.bat` - Streamlit startup script (Windows)
- `MIGRATION_GUIDE.md` - This file
- `.completed_files.txt` - Tracks completed files (auto-generated)

### Modified Files
- `requirements.txt` - Changed from Flask to Streamlit
- `README.md` - Updated documentation
- `QUICK_START.md` - Updated instructions

### Legacy Files (Kept for Reference)
- `index.html` - Original HTML interface
- `styles.css` - Original stylesheet
- `script.js` - Original JavaScript logic
- `server.py` - Original Flask backend
- `start_server.sh` - Original startup script (Unix)
- `start_server.bat` - Original startup script (Windows)

## Starting the Application 🚀

### Before (Flask)
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
./start_server.sh
# or
python server.py

# Access at http://localhost:5001
```

### After (Streamlit)
```bash
# Install dependencies
pip install -r requirements.txt

# Start app
./start_streamlit.sh
# or
streamlit run streamlit_app.py

# Access at http://localhost:8501 (auto-opens)
```

## Code Structure Comparison 📊

### Flask Version
```
┌─────────────────┐
│   index.html    │  ← User Interface
│   styles.css    │
│   script.js     │  ← Frontend Logic
└────────┬────────┘
         │ HTTP/API
┌────────▼────────┐
│   server.py     │  ← Backend Logic
│   (Flask)       │  ← File Storage
└─────────────────┘
```

### Streamlit Version
```
┌─────────────────┐
│ streamlit_app.py│  ← UI + Logic + Storage
│  (All-in-one)   │  ← Single Python File
└─────────────────┘
```

## Benefits of Streamlit Version 🎯

1. **Faster Development**: Write UI and logic in pure Python
2. **Real-time Updates**: Instant feedback without page reloads
3. **Better Debugging**: Python stack traces instead of JS console errors
4. **Easier Deployment**: Single file deployment (can use Streamlit Cloud)
5. **Built-in Components**: Progress bars, download buttons, etc.
6. **Type Safety**: Python type hints throughout
7. **Data Integration**: Seamless pandas integration
8. **Maintainability**: One language, one file

## Potential Future Enhancements 🔮

With Streamlit, these features are easier to add:

1. **Database Integration**: Add SQLite/PostgreSQL for better data tracking
2. **User Authentication**: Streamlit supports authentication plugins
3. **Data Visualization**: Built-in charting with st.plotly_chart, st.altair_chart
4. **File Upload**: Add CSV upload functionality (st.file_uploader)
5. **Export Formats**: Support Excel, JSON exports via pandas
6. **Advanced Filtering**: Filter files by date, user, status
7. **Analytics Dashboard**: Show labeling statistics and trends
8. **Multi-user Support**: Session management for multiple users
9. **Cloud Deployment**: Deploy to Streamlit Cloud for free
10. **Mobile Optimization**: Streamlit is mobile-responsive by default

## Rollback Instructions 🔙

If you need to use the Flask version:

1. **Keep both versions**: All Flask files are still present
2. **Switch requirements**:
   ```bash
   pip uninstall streamlit pandas
   pip install Flask==3.0.0 flask-cors==4.0.0
   ```
3. **Start Flask server**:
   ```bash
   ./start_server.sh
   # or
   python server.py
   ```
4. **Access at**: http://localhost:5001

## Questions? 💬

- **Q: Can I use both versions simultaneously?**
  - A: Yes! They run on different ports (Flask: 5001, Streamlit: 8501)

- **Q: Will my data be lost?**
  - A: No! Both versions use the same `./results/` directory

- **Q: How do I deploy Streamlit to production?**
  - A: See [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/get-started)

- **Q: Can I customize the Streamlit theme?**
  - A: Yes! Create a `.streamlit/config.toml` file for theming

## Resources 📚

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Components](https://streamlit.io/components)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Streamlit Forum](https://discuss.streamlit.io/)

---

**Conversion Date**: November 3, 2025
**Streamlit Version**: 1.28.0+
**Python Version**: 3.8+

