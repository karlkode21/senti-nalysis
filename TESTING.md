# Testing Guide 🧪

This guide will help you test the Streamlit Senti-Nalysis application.

## Prerequisites ✅

Before testing, ensure:
- Python 3.8+ is installed
- Dependencies are installed: `pip install -r requirements.txt`
- CSV files exist in `./documents/` directory

## Quick Test 🚀

### 1. Start the Application

```bash
streamlit run streamlit_app.py
```

The app should:
- Start without errors
- Open automatically in your browser
- Display at `http://localhost:8501`

### 2. Verify UI Elements

Check that the following are visible:
- ✅ Logo (if image exists in `./images/`)
- ✅ Main header with gradient background
- ✅ File selection dropdown
- ✅ File list populated from `./documents/`

## Test Scenarios 📋

### Scenario 1: Complete Labeling Flow

**Steps:**
1. Select a CSV file from dropdown
2. Enter username (e.g., "Test User")
3. Click "🚀 Start Labeling"
4. Verify record displays:
   - User field shows correct data
   - Text field shows full text
   - Progress bar shows "Record 1 of N"
5. Click sentiment button (Positive, Neutral, or Negative)
6. Click "✅ Submit & Next"
7. Repeat until all records are labeled
8. Verify completion screen shows:
   - Success message
   - Summary statistics
   - Download button
9. Click "📥 Download Report"
10. Verify file downloads with correct filename format
11. Check `./results/` folder for saved file

**Expected Result:**
- ✅ CSV file downloads successfully
- ✅ File saved to `./results/` directory
- ✅ Filename format: `{username}_{filename}-{timestamp}.csv`
- ✅ CSV contains 3 columns: user, text, sentiment_by_{username}
- ✅ File marked as completed in dropdown

### Scenario 2: Completed File Prevention

**Steps:**
1. Complete labeling for a file (follow Scenario 1)
2. Click "🔄 Start New Session"
3. Look at dropdown list
4. Verify completed file shows "✅ ... (Completed)"
5. Try to select the completed file

**Expected Result:**
- ✅ Completed file is disabled/shows warning
- ✅ Cannot start labeling on completed file

### Scenario 3: Reset Completed Files

**Steps:**
1. Complete at least one file
2. Verify "🔄 Reset Completed Files" button is visible
3. Click the button
4. Check dropdown list

**Expected Result:**
- ✅ Button appears after completing a file
- ✅ All files become available again after reset
- ✅ `.completed_files.txt` is cleared

### Scenario 4: Progress Tracking

**Steps:**
1. Start labeling a file
2. Label a few records (not all)
3. Watch progress bar and counter
4. Note sidebar information

**Expected Result:**
- ✅ Progress bar updates after each submission
- ✅ Counter shows "Record X of Y"
- ✅ Sidebar shows username, file, and progress
- ✅ Progress percentage increases correctly

### Scenario 5: Empty Documents Folder

**Steps:**
1. Temporarily move all CSV files out of `./documents/`
2. Restart the app
3. Check for error handling

**Expected Result:**
- ✅ App shows "No CSV files found" message
- ✅ No crash or exceptions

### Scenario 6: Invalid CSV File

**Steps:**
1. Create a CSV file without required columns
2. Place it in `./documents/`
3. Restart app and select the file
4. Try to start labeling

**Expected Result:**
- ✅ Error message displayed
- ✅ App doesn't crash
- ✅ User can select another file

## Manual UI Tests 🎨

### Visual Elements
- [ ] Logo displays correctly
- [ ] Header has gradient background
- [ ] Record cards have proper styling
- [ ] Buttons have correct emojis and colors
- [ ] Progress bar is visible and styled
- [ ] Sidebar information is readable

### Responsiveness
- [ ] Test on desktop browser (full width)
- [ ] Test on narrow browser window
- [ ] Check text wrapping in record cards
- [ ] Verify buttons stack properly on small screens

### Interactions
- [ ] Buttons show hover effects
- [ ] Selected sentiment button highlighted
- [ ] Submit button enables only after selection
- [ ] Transitions between screens are smooth
- [ ] Loading states are clear

## Performance Tests ⚡

### Large File Handling

**Test with large CSV (100+ records):**
1. Create or use a large CSV file
2. Load and label records
3. Monitor performance

**Expected:**
- ✅ App loads file quickly
- ✅ No lag between submissions
- ✅ Progress bar updates smoothly
- ✅ Download completes successfully

## Integration Tests 🔗

### File System Operations

**Test file operations:**
```bash
# Check results directory is created
ls -la results/

# Verify file permissions
touch results/test.txt && rm results/test.txt

# Check completed files tracking
cat .completed_files.txt
```

### CSV Validation

**Test CSV output:**
1. Complete labeling and download
2. Open CSV in spreadsheet software
3. Verify:
   - ✅ Proper CSV formatting
   - ✅ Quoted fields with commas
   - ✅ UTF-8 encoding
   - ✅ All records present
   - ✅ No duplicate headers

## Error Handling Tests 🚨

### Network/Port Issues

**Test port conflicts:**
```bash
# Start two instances
streamlit run streamlit_app.py
streamlit run streamlit_app.py  # Should use different port
```

**Expected:**
- ✅ Second instance uses different port
- ✅ Clear error message if port unavailable

### File Permission Errors

**Test restricted permissions:**
```bash
# Make results directory read-only
chmod 444 results/
# Try to complete labeling
# Restore permissions
chmod 755 results/
```

**Expected:**
- ✅ Error message displayed
- ✅ App doesn't crash
- ✅ User can continue with other actions

## Browser Compatibility 🌐

Test on multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

For each browser, verify:
- App loads correctly
- All buttons work
- Download functionality works
- Session state persists

## Automated Testing (Optional) 🤖

For automated testing, consider using:

```python
# test_streamlit_app.py
import pytest
from streamlit_app import load_csv_file, save_report_to_results
import pandas as pd

def test_load_csv_file():
    # Test CSV loading
    df = load_csv_file("sample_data.csv")
    assert df is not None
    assert 'user' in df.columns
    assert 'text' in df.columns

def test_save_report():
    # Test report saving
    test_df = pd.DataFrame({
        'user': ['test'],
        'text': ['test text'],
        'sentiment_by_test': ['positive']
    })
    filename = save_report_to_results("test", "test.csv", test_df)
    assert filename is not None
    assert 'test_test-' in filename
```

Run with: `pytest test_streamlit_app.py`

## Common Issues & Solutions 🔧

### Issue: App won't start
**Solution:** Check Python version, reinstall dependencies
```bash
python --version  # Should be 3.8+
pip install --upgrade streamlit pandas
```

### Issue: CSV files not showing
**Solution:** Check documents directory exists and has CSV files
```bash
ls -la documents/
```

### Issue: Download button doesn't work
**Solution:** Check browser popup blocker, try different browser

### Issue: Session state lost
**Solution:** This is expected behavior - session state is per-session. Don't refresh page.

### Issue: Results not saving
**Solution:** Check results directory permissions
```bash
ls -ld results/
chmod 755 results/
```

## Test Checklist ✅

Before deploying or sharing:

- [ ] All test scenarios pass
- [ ] No console errors in browser
- [ ] CSV download works
- [ ] File tracking works
- [ ] UI looks good on desktop and mobile
- [ ] Documentation is up to date
- [ ] Requirements.txt is correct
- [ ] Startup scripts work
- [ ] Sample data file works
- [ ] Results directory saves correctly

## Continuous Testing 🔄

For ongoing development:

1. **Before each commit:**
   - Run quick test (Scenario 1)
   - Check for console errors
   - Verify no linter errors

2. **Before releases:**
   - Run all test scenarios
   - Test on multiple browsers
   - Verify documentation accuracy

3. **After deployment:**
   - Test in production environment
   - Verify all features work
   - Check performance with real data

## Reporting Issues 🐛

When reporting issues, include:
- Streamlit version: `streamlit --version`
- Python version: `python --version`
- Operating system
- Browser and version
- Steps to reproduce
- Expected vs actual behavior
- Console error messages
- Screenshots if relevant

---

**Happy Testing! 🎉**

For questions or issues, refer to the main README.md or MIGRATION_GUIDE.md.

