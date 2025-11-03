# Save & Resume Feature Guide 💾

## Overview

The Save & Resume feature allows you to save your labeling progress at any time and resume later, even after closing your browser or restarting your computer.

---

## How It Works 🔄

### File-Based Storage
Progress is saved to: `.progress/current_session.json`

This file contains:
- Username
- Selected CSV file
- Current record index
- All labels assigned so far
- Total number of records
- Timestamp of when progress was saved

### Persistence
Unlike browser-based storage (localStorage), file-based storage means:
- ✅ Works across different browsers
- ✅ Survives browser restarts
- ✅ Survives computer restarts
- ✅ Can be backed up easily
- ✅ Can be manually inspected/edited if needed

---

## Using Save & Resume 📚

### Saving Your Progress

**Option 1: Manual Save**
1. While labeling, look at the sidebar
2. Click the **"💾 Save & Exit"** button
3. You'll see a success message
4. The app returns to the home screen

**Option 2: Automatic on Exit**
- If you close the browser while labeling, your progress is **NOT** automatically saved
- Always use "Save & Exit" button to preserve your work

### Resuming Your Session

1. **Start the app** (any time after saving):
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Resume Screen appears** automatically if saved progress exists

3. **View progress details**:
   - File name
   - Your username
   - Number of records completed
   - Percentage complete
   - When it was saved

4. **Choose an action**:
   - **📂 Resume Session** - Continue labeling where you left off
   - **🆕 Start New Session** - Begin a new file (keeps saved progress)
   - **🗑️ Delete Saved Progress** - Remove saved progress permanently

---

## Resume Screen Example 🖼️

```
┌─────────────────────────────────────────────────────────┐
│  🔄 Resume Previous Session?                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📊 Saved Progress          │  🎯 Choose Action         │
│                              │                           │
│  File: Tutor room B_Warner  │  [📂 Resume Session]     │
│  User: John Doe             │  [🆕 Start New Session]  │
│  Progress: 25 of 61 records │                           │
│  40.9% complete             │  ───────────────         │
│  [████████░░░░░░░░░░░]      │                           │
│  Saved: November 3, 2025    │  [🗑️ Delete Progress]   │
│         at 2:45 PM          │                           │
│                              │                           │
└─────────────────────────────────────────────────────────┘
```

---

## Important Notes ⚠️

### Single Session Limit
- Only **one progress session** can be saved at a time
- Saving a new session **overwrites** the previous one
- Complete your current file before starting another

### Browser Refresh
- **Pressing F5 or refreshing** the page will **lose unsaved progress**
- Always use "💾 Save & Exit" before closing or refreshing

### Manual Progress Management
You can manually manage progress files:

**View progress:**
```bash
cat .progress/current_session.json
```

**Backup progress:**
```bash
cp .progress/current_session.json .progress/backup_$(date +%Y%m%d_%H%M%S).json
```

**Delete progress:**
```bash
rm .progress/current_session.json
```

---

## Workflow Examples 🎯

### Example 1: Long Labeling Session

```
Day 1 (2:00 PM):
1. Start app
2. Select file "Tutor room B_Warner"
3. Label 25 out of 61 records
4. Click "💾 Save & Exit"
5. Close browser

Day 2 (9:00 AM):
1. Start app
2. See resume screen
3. Click "📂 Resume Session"
4. Continue from record 26
5. Complete all 61 records
6. Download report
```

### Example 2: Multiple Files

```
File 1:
1. Start labeling file A
2. Complete 50% of records
3. Click "💾 Save & Exit"

File 2 (Later):
1. Start app
2. See resume screen for file A
3. Choose "🆕 Start New Session"  ← Progress still saved
4. Select file B
5. Start labeling file B
6. Exit without saving file B

Next Time:
1. Start app
2. See resume screen for FILE A (not B)
3. File A progress was preserved
```

### Example 3: Accidental Close

```
Scenario: Browser crashes or system restarts

Without Save & Exit:
❌ Progress is lost
❌ Must start over

With Save & Exit:
✅ Progress is preserved
✅ Resume when you return
```

---

## Troubleshooting 🔧

### Issue: Resume screen doesn't appear

**Possible causes:**
1. No progress file exists
2. Progress file was deleted
3. Progress file is corrupted

**Solution:**
```bash
# Check if file exists
ls -la .progress/current_session.json

# View contents
cat .progress/current_session.json

# If corrupted, delete and start fresh
rm .progress/current_session.json
```

### Issue: Can't load saved progress

**Error message:** "Failed to load progress"

**Possible causes:**
1. CSV file was moved or deleted
2. JSON file is corrupted
3. File permissions issue

**Solution:**
1. Check that CSV file still exists in `./documents/`
2. Try deleting progress and starting new: Click "🗑️ Delete Saved Progress"
3. Check file permissions: `ls -l .progress/`

### Issue: Wrong progress showing

**Problem:** Seeing progress from a different session

**Solution:**
- Click "🗑️ Delete Saved Progress"
- Or manually delete: `rm .progress/current_session.json`
- Start fresh session

---

## Best Practices ✨

### 1. Save Regularly
- Save after every 10-20 records
- Save before taking breaks
- Save before closing browser

### 2. Complete Files
- Try to complete one file before starting another
- Only one progress session is saved at a time

### 3. Backup Important Progress
```bash
# Create a backup before risky operations
cp .progress/current_session.json .progress/backup.json
```

### 4. Clean Up When Done
- Progress is automatically deleted when you complete and download a file
- No manual cleanup needed

---

## Technical Details 🛠️

### Progress File Format

```json
{
  "username": "John_Doe",
  "selected_file": "Tutor room B_Warner.csv",
  "current_index": 25,
  "user_labels": [
    "positive",
    "neutral",
    "negative",
    ...
  ],
  "total_records": 61,
  "timestamp": "2025-11-03T14:45:32.123456"
}
```

### Storage Location
- **Directory**: `.progress/`
- **File**: `current_session.json`
- **Full path**: `/path/to/Senti-Nalysis/v.3.0.0/.progress/current_session.json`

### File Size
- Typically very small (< 10 KB)
- Grows with number of records
- Safe to keep indefinitely

### Security
- Stored locally on your machine
- Not transmitted over network
- No sensitive data (just labels and filenames)

---

## Comparison: Old vs New 📊

| Aspect | Flask (localStorage) | Streamlit (File-based) |
|--------|---------------------|------------------------|
| Persistence | Browser only | Across system |
| Survives reboot | ❌ | ✅ |
| Works on different browser | ❌ | ✅ |
| Can backup | ❌ | ✅ |
| Survives browser clear | ❌ | ✅ |
| Manual inspection | ❌ | ✅ |
| Multi-user | ❌ | ⚠️ (one session) |

---

## FAQ ❓

**Q: Can I save multiple sessions?**
A: No, only one session is saved at a time. Complete current file before starting another.

**Q: What happens if I start a new file without resuming?**
A: Your old progress is kept unless you explicitly delete it or save progress on the new file.

**Q: Can I edit the progress file manually?**
A: Yes, but not recommended. The JSON format must be valid.

**Q: Is my progress backed up?**
A: No automatic backup. Use the backup command if needed.

**Q: Can multiple users have separate progress?**
A: No, only one progress file exists. For multi-user, implement user-specific progress files.

**Q: What if I complete the file?**
A: Progress is automatically deleted when you download the report.

---

## Advanced: Multiple User Support 🚀

To support multiple users, you could modify the code to save progress as:
```
.progress/{username}_current_session.json
```

This would allow each user to have their own saved progress. This feature is not currently implemented but could be added if needed.

---

## Support 💬

For issues or questions:
1. Check this guide
2. Review `TESTING.md` for troubleshooting
3. Check `README.md` for general info
4. Inspect `.progress/current_session.json` for debugging

---

**Enjoy uninterrupted labeling with Save & Resume! 💾✨**

