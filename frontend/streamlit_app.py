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
        st.error(f"Errore di comunicazione con il backend: {e}")
        return None

# --- UI LAYOUT ---
st.title("📊 Data Insight Explorer")
st.write("Carica un file CSV o XLSX per analizzare le statistiche.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "Scegli un file",
    type=["csv", "xlsx"],
    help="I file caricati vengono elaborati in memoria e non vengono salvati."
)

if uploaded_file is not None:
    # Check if this is a new file upload
    if uploaded_file.name != st.session_state.last_uploaded_filename:
        with st.spinner("Elaborazione del nuovo file..."):
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
    st.header("Risultati dell'Analisi")

    st.subheader("Statistiche Descrittive")
    # The backend returns stats as a dict, convert to DataFrame for nice display
    stats_df = pd.DataFrame(results.get("stats", {}))
    st.dataframe(stats_df)

else:
    st.info("In attesa del caricamento di un file...")