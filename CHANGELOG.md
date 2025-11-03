# Changelog 📝

All notable changes to the Senti-Nalysis project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2025-11-03

### 🎉 Major Release - Streamlit Conversion

This version represents a complete rewrite of the application using Streamlit, replacing the Flask-based architecture.

### Added
- **New Streamlit Application** (`streamlit_app.py`)
  - Single Python file containing all application logic
  - Modern, interactive UI with real-time updates
  - Built-in session state management
  - Custom CSS styling with gradients and modern design
  - Sidebar with progress information and controls
  - Summary statistics on completion screen
  
- **New Configuration Files**
  - `.streamlit/config.toml` - Streamlit theme and server configuration
  - `.gitignore` - Version control exclusions
  
- **New Startup Scripts**
  - `start_streamlit.sh` - Unix/Linux startup script
  - `start_streamlit.bat` - Windows startup script
  
- **Comprehensive Documentation**
  - `MIGRATION_GUIDE.md` - Detailed Flask to Streamlit migration guide
  - `TESTING.md` - Complete testing procedures and scenarios
  - `DEPLOYMENT.md` - Multi-platform deployment instructions
  - `CHANGELOG.md` - This file
  
- **New Features**
  - Real-time progress tracking in sidebar
  - File-based completion tracking (`.completed_files.txt`)
  - Summary statistics (Positive/Neutral/Negative counts)
  - Improved error handling and user feedback
  - Mobile-responsive design
  - Custom theme with purple gradient branding

### Changed
- **Framework Migration**: Flask → Streamlit
  - Removed HTML/CSS/JavaScript frontend
  - Removed Flask backend server
  - All UI and logic now in Python
  
- **State Management**: localStorage → Session State
  - Client-side localStorage replaced with server-side session state
  - Completion tracking moved from browser to file system
  
- **Dependencies** (`requirements.txt`)
  - Removed: Flask, flask-cors
  - Added: streamlit, pandas
  
- **Port**: 5001 → 8501 (default Streamlit port)

- **Documentation Updates**
  - `README.md` - Completely rewritten for Streamlit
  - `QUICK_START.md` - Updated with Streamlit instructions

### Enhanced
- **Save & Resume Feature**
  - Re-implemented using file-based storage (`.progress/current_session.json`)
  - Progress persists across browser sessions and computer restarts
  - Resume screen shows detailed progress information
  - Option to delete saved progress if needed

### Technical Improvements
- **Better Data Handling**: Using pandas for all CSV operations
- **Simplified Architecture**: Single file vs. multiple frontend/backend files
- **Improved Performance**: Direct Python data processing vs. API calls
- **Better Type Safety**: Python throughout (no JavaScript type issues)
- **Easier Maintenance**: One language, clearer code structure

### Migration Notes
- Flask version files were removed after successful testing
- Results directory and CSV files remain unchanged
- Clean workspace with only Streamlit files
- No data migration required

### Breaking Changes
- ⚠️ **Port changed**: Now runs on 8501 instead of 5001
- ⚠️ **Startup command changed**: `streamlit run streamlit_app.py` instead of `python server.py`
- ⚠️ **Progress storage location**: Now in `.progress/` directory instead of browser localStorage

### Known Issues
- Session state lost on browser refresh (use Save & Exit to preserve progress)
- Large CSV files (1000+ rows) may cause slower initial load
- Progress tracking is per-installation (not per-user)
- Only one progress session can be saved at a time

### Future Enhancements (Planned)
- [x] Add persistent save/resume functionality ✅ (v3.0.1)
- [ ] Multiple user progress tracking
- [ ] User authentication system
- [ ] Database integration for better tracking
- [ ] Advanced analytics dashboard
- [ ] Export to multiple formats (Excel, JSON)
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Keyboard shortcuts for faster labeling

---

## [2.0.0] - 2023-11-XX

### Added
- Flask backend with API endpoints
- Automatic file saving to `./results/` directory
- File completion tracking with localStorage
- Reset completed files functionality
- Backend health check endpoint

### Changed
- Improved UI with modern gradients and animations
- Enhanced CSV parsing for quoted fields
- Better error handling

### Fixed
- CSV escaping issues with commas and quotes
- Progress persistence bugs

---

## [1.0.0] - 2023-XX-XX

### Added
- Initial release
- Basic sentiment labeling functionality
- File selection from documents folder
- Progress tracking
- CSV report generation
- Save & Resume feature
- Responsive UI design

---

## Version Comparison

| Feature | v1.0 | v2.0 (Flask) | v3.0 (Streamlit) |
|---------|------|--------------|------------------|
| Frontend | HTML/CSS/JS | HTML/CSS/JS | Streamlit |
| Backend | Client-only | Flask | Streamlit |
| Port | 5000 | 5001 | 8501 |
| State Management | localStorage | localStorage | Session + File |
| Backend Storage | ❌ | ✅ | ✅ |
| Save/Resume | ✅ | ✅ | ✅ |
| Resume After Reboot | ❌ | ❌ | ✅ |
| Completion Tracking | ✅ | ✅ | ✅ |
| File Dependencies | 3+ | 4+ | 1 |
| Lines of Code | ~800 | ~900 | ~630 |
| Setup Complexity | Medium | Medium | Low |
| Deployment Options | Limited | Limited | Many |

---

## Migration Paths

### From v1.0 to v2.0
- Update requirements.txt
- Add server.py
- Update startup scripts
- No data changes needed

### From v2.0 to v3.0
- Install Streamlit: `pip install streamlit pandas`
- Run new app: `streamlit run streamlit_app.py`
- Old Flask files can coexist
- Results directory remains compatible
- See MIGRATION_GUIDE.md for details

### Rolling Back from v3.0 to v2.0
- Install Flask: `pip install Flask flask-cors`
- Run old server: `python server.py`
- All data remains intact
- No migration needed

---

## Contributing

See the main README.md for contribution guidelines.

## Support

For questions or issues:
- Check documentation in README.md, QUICK_START.md, MIGRATION_GUIDE.md
- Review TESTING.md for common issues
- Check DEPLOYMENT.md for deployment problems

---

**Version 3.0.0 - Built with ❤️ using Streamlit**

