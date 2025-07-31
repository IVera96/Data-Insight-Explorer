import streamlit as st
import requests
import pandas as pd
import io

# Set a title for the browser tab
st.set_page_config(page_title="Data Insight Explorer", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "uploaded_file_bytes" not in st.session_state:
    st.session_state.uploaded_file_bytes = None
if "last_uploaded_filename" not in st.session_state:
    st.session_state.last_uploaded_filename = None

# --- API COMMUNICATION ---
def get_backend_analysis(file_bytes):
    """Function to send data to the backend API and get results."""
    files = {'file': ('data.csv', file_bytes, 'text/csv')}
    try:
        # The URL must use the Docker service name, 'api'
        response = requests.post("http://api:8000/upload/", files=files)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the backend: {e}")
        return None

# --- UI LAYOUT ---
st.title("📊 Data Insight Explorer")
st.write("Upload a CSV or XLSX file to analyze statistics.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "Choose a file",
    type=["csv", "xlsx"],
    help="Uploaded files are processed in memory and are not saved."
)

if uploaded_file is not None:
    # Check if this is a new file upload
    if uploaded_file.name != st.session_state.last_uploaded_filename:
        with st.spinner("Processing the new file..."):
            # Reset state for the new file
            st.session_state.last_uploaded_filename = uploaded_file.name

            # Convert file to bytes, which is what the API expects
            if uploaded_file.type == "text/csv":
                file_bytes = uploaded_file.getvalue()
            else:  # Handle XLSX
                df = pd.read_excel(uploaded_file)
                # Convert to CSV bytes
                buf = io.StringIO()
                df.to_csv(buf, index=False)
                file_bytes = buf.getvalue().encode('utf-8')
            
            st.session_state.uploaded_file_bytes = file_bytes
            
            # Perform the initial analysis
            st.session_state.analysis_results = get_backend_analysis(file_bytes)

# --- DISPLAY RESULTS ---
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    st.write("---")
    st.header("Analysis Results")

    st.subheader("Descriptive Statistics")
    # The backend returns stats as a dict, convert to DataFrame for nice display
    stats_df = pd.DataFrame(results.get("stats", {}))
    st.dataframe(stats_df)

else:
    st.info("Waiting for a file to be uploaded...")