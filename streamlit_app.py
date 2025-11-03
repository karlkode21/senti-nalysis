#!/usr/bin/env python3
"""
Senti-Nalysis - Streamlit Sentiment Labeling Tool
A modern web application for labeling text sentiment
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import base64

# Page configuration
st.set_page_config(
    page_title="Senti-Nalysis - Sentiment Labeling Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .record-card {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .sentiment-button {
        width: 100%;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border: 2px solid #ddd;
        cursor: pointer;
        transition: all 0.3s;
    }
    .progress-container {
        background: #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'check_resume'  # check_resume, file_selection, labeling, complete
    if 'csv_data' not in st.session_state:
        st.session_state.csv_data = None
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'user_labels' not in st.session_state:
        st.session_state.user_labels = []
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'selected_file' not in st.session_state:
        st.session_state.selected_file = None
    if 'completed_files' not in st.session_state:
        st.session_state.completed_files = load_completed_files()
    if 'current_sentiment' not in st.session_state:
        st.session_state.current_sentiment = None
    if 'saved_progress' not in st.session_state:
        st.session_state.saved_progress = check_for_saved_progress()
    if 'progress_session_id' not in st.session_state:
        st.session_state.progress_session_id = None

# File management functions
def get_available_files():
    """Get list of CSV files from documents directory"""
    documents_dir = Path(__file__).parent / 'documents'
    if not documents_dir.exists():
        return []
    
    files = sorted([f.name for f in documents_dir.glob('*.csv')])
    return files

def load_completed_files():
    """Load list of completed files from a tracking file"""
    completed_file = Path(__file__).parent / '.completed_files.txt'
    if completed_file.exists():
        with open(completed_file, 'r') as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_completed_files(completed_files):
    """Save list of completed files"""
    completed_file = Path(__file__).parent / '.completed_files.txt'
    with open(completed_file, 'w') as f:
        f.write('\n'.join(completed_files))

def mark_file_as_completed(filename):
    """Mark a file as completed"""
    if filename not in st.session_state.completed_files:
        st.session_state.completed_files.append(filename)
        save_completed_files(st.session_state.completed_files)

def reset_completed_files():
    """Reset all completed files"""
    st.session_state.completed_files = []
    completed_file = Path(__file__).parent / '.completed_files.txt'
    if completed_file.exists():
        completed_file.unlink()

# Progress management functions
def get_progress_file_path():
    """Get path to the progress file"""
    progress_dir = Path(__file__).parent / '.progress'
    progress_dir.mkdir(exist_ok=True)
    return progress_dir / 'current_session.json'

def check_for_saved_progress():
    """Check if there is saved progress"""
    import json
    progress_file = get_progress_file_path()
    
    if progress_file.exists():
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
            return progress_data
        except Exception as e:
            st.error(f"Error loading progress: {str(e)}")
            return None
    return None

def save_progress_to_file():
    """Save current progress to file"""
    import json
    from datetime import datetime
    
    progress_file = get_progress_file_path()
    
    progress_data = {
        'username': st.session_state.username,
        'selected_file': st.session_state.selected_file,
        'current_index': st.session_state.current_index,
        'user_labels': st.session_state.user_labels,
        'total_records': len(st.session_state.csv_data) if st.session_state.csv_data is not None else 0,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving progress: {str(e)}")
        return False

def clear_saved_progress():
    """Clear saved progress file"""
    progress_file = get_progress_file_path()
    if progress_file.exists():
        try:
            progress_file.unlink()
        except Exception as e:
            st.error(f"Error clearing progress: {str(e)}")

def load_progress_from_file(progress_data):
    """Load progress from saved data"""
    try:
        # Load the CSV file
        df = load_csv_file(progress_data['selected_file'])
        
        if df is not None:
            st.session_state.csv_data = df
            st.session_state.username = progress_data['username']
            st.session_state.selected_file = progress_data['selected_file']
            st.session_state.current_index = progress_data['current_index']
            st.session_state.user_labels = progress_data['user_labels']
            st.session_state.stage = 'labeling'
            return True
        return False
    except Exception as e:
        st.error(f"Error loading progress: {str(e)}")
        return False

# Data processing functions
def load_csv_file(filename):
    """Load and parse CSV file"""
    documents_dir = Path(__file__).parent / 'documents'
    file_path = documents_dir / filename
    
    try:
        df = pd.read_csv(file_path)
        # Convert column names to lowercase
        df.columns = df.columns.str.lower().str.strip()
        
        # Validate required columns
        required_columns = ['user', 'text']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"CSV must contain columns: {', '.join(required_columns)}")
            return None
        
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def save_report_to_results(username, filename, csv_content):
    """Save completed report to results directory"""
    results_dir = Path(__file__).parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    # Clean username
    clean_username = username.replace(' ', '_')
    
    # Remove .csv extension from filename
    filename_without_ext = filename.replace('.csv', '')
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create filename
    output_filename = f"{clean_username}_{filename_without_ext}-{timestamp}.csv"
    output_path = results_dir / output_filename
    
    # Save file
    csv_content.to_csv(output_path, index=False)
    
    return output_filename

# Navigation functions
def start_labeling():
    """Start the labeling process"""
    st.session_state.stage = 'labeling'
    st.session_state.current_index = 0
    st.session_state.user_labels = [None] * len(st.session_state.csv_data)
    st.session_state.current_sentiment = None

def submit_label(sentiment):
    """Submit current label and move to next record"""
    st.session_state.user_labels[st.session_state.current_index] = sentiment
    st.session_state.current_index += 1
    st.session_state.current_sentiment = None
    
    # Check if all records are labeled
    if st.session_state.current_index >= len(st.session_state.csv_data):
        st.session_state.stage = 'complete'

def reset_app():
    """Reset app to initial state"""
    clear_saved_progress()
    st.session_state.stage = 'check_resume'
    st.session_state.csv_data = None
    st.session_state.current_index = 0
    st.session_state.user_labels = []
    st.session_state.username = ''
    st.session_state.selected_file = None
    st.session_state.current_sentiment = None
    st.session_state.saved_progress = None

def save_and_exit():
    """Save progress and return to home"""
    if save_progress_to_file():
        st.success("✅ Progress saved successfully!")
        st.info("You can resume from where you left off when you return.")
        st.session_state.stage = 'check_resume'
        st.session_state.saved_progress = check_for_saved_progress()
        st.rerun()

def download_csv_data(df, filename):
    """Generate CSV download data"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return b64

# Main application
def main():
    """Main application logic"""
    init_session_state()
    
    # Header with logo
    logo_path = Path(__file__).parent / 'images' / 'Senti-Nalysis_logo.png'
    if logo_path.exists():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(str(logo_path), use_column_width=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Sentiment Labeling Tool</h1>
        <p>Select, Label, and Download Your Sentiment Analysis Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Information")
        
        if st.session_state.stage == 'labeling':
            st.metric("Current User", st.session_state.username)
            st.metric("Selected File", st.session_state.selected_file)
            st.metric("Progress", f"{st.session_state.current_index}/{len(st.session_state.csv_data)}")
            
            st.divider()
            
            if st.button("💾 Save & Exit", use_container_width=True, type="secondary"):
                save_and_exit()
        
        st.divider()
        st.info("💡 **Tips:**\n- Read each text carefully\n- Label based on overall sentiment\n- Save your work regularly")
    
    # Main content based on stage
    if st.session_state.stage == 'check_resume':
        show_resume_screen()
    elif st.session_state.stage == 'file_selection':
        show_file_selection_screen()
    elif st.session_state.stage == 'labeling':
        show_labeling_screen()
    elif st.session_state.stage == 'complete':
        show_complete_screen()

def show_resume_screen():
    """Display resume or start new session screen"""
    if st.session_state.saved_progress:
        progress = st.session_state.saved_progress
        
        st.markdown("""
        <div class="info-box">
            <h2 style="margin-top:0;">🔄 Resume Previous Session?</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Saved Progress")
            st.write(f"**File:** {progress['selected_file']}")
            st.write(f"**User:** {progress['username']}")
            st.write(f"**Progress:** {progress['current_index']} of {progress['total_records']} records")
            
            # Calculate percentage
            if progress['total_records'] > 0:
                percentage = (progress['current_index'] / progress['total_records']) * 100
                st.progress(progress['current_index'] / progress['total_records'])
                st.write(f"**{percentage:.1f}% complete**")
            
            # Show timestamp
            from datetime import datetime
            try:
                timestamp = datetime.fromisoformat(progress['timestamp'])
                st.write(f"**Saved:** {timestamp.strftime('%B %d, %Y at %I:%M %p')}")
            except:
                pass
        
        with col2:
            st.markdown("### 🎯 Choose Action")
            st.write("")
            st.write("")
            
            if st.button("📂 Resume Session", use_container_width=True, type="primary"):
                if load_progress_from_file(progress):
                    st.success("✅ Progress loaded successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to load progress. Starting new session.")
                    st.session_state.stage = 'file_selection'
                    st.session_state.saved_progress = None
                    st.rerun()
            
            if st.button("🆕 Start New Session", use_container_width=True, type="secondary"):
                clear_saved_progress()
                st.session_state.stage = 'file_selection'
                st.session_state.saved_progress = None
                st.rerun()
            
            st.divider()
            
            if st.button("🗑️ Delete Saved Progress", use_container_width=True):
                clear_saved_progress()
                st.session_state.saved_progress = None
                st.success("✅ Saved progress deleted!")
                st.rerun()
    else:
        # No saved progress, go directly to file selection
        st.session_state.stage = 'file_selection'
        st.rerun()

def show_file_selection_screen():
    """Display file selection screen"""
    st.header("📁 Select a CSV File")
    
    # Get available files
    available_files = get_available_files()
    
    if not available_files:
        st.error("No CSV files found in the 'documents' directory!")
        return
    
    # Show reset button if there are completed files
    if st.session_state.completed_files:
        st.markdown(f"""
        <div class="info-box">
            ✅ {len(st.session_state.completed_files)} file(s) completed
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Reset Completed Files", use_container_width=True):
            reset_completed_files()
            st.success("All files have been reset!")
            st.rerun()
    
    # Filter out completed files for display
    uncompleted_files = [f for f in available_files if f not in st.session_state.completed_files]
    completed_files_display = [f"✅ {f} (Completed)" for f in available_files if f in st.session_state.completed_files]
    
    all_files_display = uncompleted_files + completed_files_display
    
    # File selection
    st.subheader("Choose a file to label:")
    selected_display = st.selectbox(
        "Select file",
        options=["-- Choose a file --"] + all_files_display,
        key="file_selector"
    )
    
    if selected_display and selected_display != "-- Choose a file --":
        # Extract actual filename (remove completion marker if present)
        if selected_display.startswith("✅"):
            st.warning("⚠️ This file has already been completed. Please select another file or reset completed files.")
            return
        
        selected_file = selected_display
        
        # Show file info
        st.success(f"Selected: **{selected_file}**")
        
        # Username input
        st.subheader("Enter Your Information:")
        username = st.text_input("Your Name:", key="username_input", placeholder="Enter your name")
        
        if username:
            if st.button("🚀 Start Labeling", type="primary", use_container_width=True):
                # Load the CSV file
                df = load_csv_file(selected_file)
                
                if df is not None and not df.empty:
                    st.session_state.csv_data = df
                    st.session_state.username = username
                    st.session_state.selected_file = selected_file
                    start_labeling()
                    st.rerun()
                else:
                    st.error("Failed to load CSV file or file is empty!")

def show_labeling_screen():
    """Display labeling screen"""
    if st.session_state.csv_data is None:
        st.error("No data loaded!")
        reset_app()
        st.rerun()
        return
    
    # Progress bar
    progress = (st.session_state.current_index) / len(st.session_state.csv_data)
    st.progress(progress)
    st.markdown(f"""
    <div class="progress-container">
        <h3 style="margin:0;">Progress: Record {st.session_state.current_index + 1} of {len(st.session_state.csv_data)}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current record
    current_record = st.session_state.csv_data.iloc[st.session_state.current_index]
    
    # Display record
    st.markdown(f"""
    <div class="record-card">
        <h3>📝 Current Record</h3>
        <p><strong>User:</strong> {current_record.get('user', 'Unknown')}</p>
        <hr>
        <p style="font-size: 1.1em; line-height: 1.6;">{current_record.get('text', 'No text available')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sentiment selection
    st.subheader("Select Sentiment:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("😊 Positive", key="positive_btn", use_container_width=True, type="primary" if st.session_state.current_sentiment == 'positive' else "secondary"):
            st.session_state.current_sentiment = 'positive'
    
    with col2:
        if st.button("😐 Neutral", key="neutral_btn", use_container_width=True, type="primary" if st.session_state.current_sentiment == 'neutral' else "secondary"):
            st.session_state.current_sentiment = 'neutral'
    
    with col3:
        if st.button("😞 Negative", key="negative_btn", use_container_width=True, type="primary" if st.session_state.current_sentiment == 'negative' else "secondary"):
            st.session_state.current_sentiment = 'negative'
    
    # Show current selection
    if st.session_state.current_sentiment:
        sentiment_display = {
            'positive': '😊 Positive',
            'neutral': '😐 Neutral',
            'negative': '😞 Negative'
        }
        st.info(f"Selected: **{sentiment_display[st.session_state.current_sentiment]}**")
    
    # Submit button
    st.divider()
    if st.button("✅ Submit & Next", type="primary", use_container_width=True, disabled=st.session_state.current_sentiment is None):
        submit_label(st.session_state.current_sentiment)
        st.rerun()

def show_complete_screen():
    """Display completion screen"""
    st.markdown("""
    <div class="success-box">
        <h1>✅ Labeling Complete!</h1>
        <p style="font-size: 1.2em;">You've successfully labeled all records.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", len(st.session_state.csv_data))
    
    with col2:
        positive_count = st.session_state.user_labels.count('positive')
        st.metric("Positive", positive_count)
    
    with col3:
        neutral_count = st.session_state.user_labels.count('neutral')
        negative_count = st.session_state.user_labels.count('negative')
        st.metric("Neutral / Negative", f"{neutral_count} / {negative_count}")
    
    # Prepare download data
    column_name = f"sentiment_by_{st.session_state.username.replace(' ', '_')}"
    
    download_df = pd.DataFrame({
        'user': st.session_state.csv_data['user'],
        'text': st.session_state.csv_data['text'],
        column_name: st.session_state.user_labels
    })
    
    # Save to results directory
    try:
        output_filename = save_report_to_results(
            st.session_state.username,
            st.session_state.selected_file,
            download_df
        )
        st.success(f"✅ Report saved to results directory as: **{output_filename}**")
    except Exception as e:
        st.error(f"Error saving report: {str(e)}")
    
    # Download button
    csv_data = download_df.to_csv(index=False)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    download_filename = f"sentiment_analysis_{st.session_state.username.replace(' ', '_')}_{timestamp}.csv"
    
    st.download_button(
        label="📥 Download Report",
        data=csv_data,
        file_name=download_filename,
        mime="text/csv",
        use_container_width=True,
        type="primary"
    )
    
    # Mark file as completed
    mark_file_as_completed(st.session_state.selected_file)
    
    # Clear saved progress since we're done
    clear_saved_progress()
    
    # Reset button
    st.divider()
    if st.button("🔄 Start New Session", use_container_width=True):
        reset_app()
        st.rerun()

if __name__ == "__main__":
    main()

