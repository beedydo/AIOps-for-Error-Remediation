# AIOps Incident Report Generator - Streamlit Front-End
#
# This application provides a web interface to:
# 1. Fetch the latest 'httpd_down.txt' log from MinIO.
# 2. Send the log to a Granite AI model for analysis.
# 3. Display the generated incident report.
# 4. Allow the user to download the report as a styled PDF using fpdf2.


# --- 1. Configuration ---

# AI Model Settings
INFERENCE_ENDPOINT = "https://granite-aiops.apps.cluster-hdmxf.hdmxf.sandbox689.opentlc.com"
MODEL_API_URL = f"{INFERENCE_ENDPOINT}/v1/completions"
MODEL_NAME = "granite"

# MinIO Storage Settings
MINIO_ENDPOINT = "minio-api-aiops.apps.cluster-hdmxf.hdmxf.sandbox689.opentlc.com"
MINIO_ACCESS_KEY = "minio"
MINIO_SECRET_KEY = "minio123"
MINIO_BUCKET = "logs"
LOG_FILE_NAME = "httpd_down.txt"

# --- 2. Helper Functions ---

@st.cache_data(ttl=60) # Cache the log data for 60 seconds
def read_log_from_minio(bucket_name, object_name):
    """Reads a log file's content from a MinIO bucket."""
    st.write(f"Reading '{object_name}' from bucket '{bucket_name}'...")
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f"http://{MINIO_ENDPOINT}",
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY
        )
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        content = response['Body'].read().decode('utf-8')
        st.write("✅ Successfully read log content from MinIO.")
        return content
    except Exception as e:
        st.error(f"Error reading from MinIO: {e}")
        return None

@st.cache_data(ttl=300) # Cache the model response for 5 minutes
def query_model_for_report(logs):
    """Queries the Granite model with a specific prompt to generate an incident report."""
    prompt = f"""
Generate a concise, structured AIOps incident report based on the following logs. The report must be in Markdown format and include:
1. Key metadata: INCIDENT ID, DETECTED, SEVERITY, STATUS, AFFECTED SERVICE, AFFECTED HOST, SUMMARY, and KEY ERROR LOG.
2. A ROOT CAUSE section explaining the 'why'.
3. A REMEDIATION PLAYBOOK section with exact, numbered shell commands to fix the issue.
4. A VALIDATION section with a command to confirm the fix.

--- LOGS START ---
{logs}
--- LOGS END ---
"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME, 
        "prompt": prompt,
        "max_tokens": 512
    }
    
    st.write("Querying Granite model for analysis...")
    try:
        response = requests.post(MODEL_API_URL, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        
        result = response.json()
        if 'choices' in result and result['choices']:
            report_text = result['choices'][0].get('text', 'Error: Could not extract report from model response.')
            st.write("✅ Analysis complete.")
            return report_text
        else:
            st.error(f"Unexpected response format from model: {json.dumps(result)}")
            return None
    except Exception as e:
        st.error(f"Error connecting to model at `{MODEL_API_URL}`. Details: {e}")
        return None

def generate_pdf(markdown_text):
    """Converts a Markdown string to a PDF using FPDF2."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=10)

    lines = markdown_text.split('\n')
    
    for line in lines:
        if line.startswith("### "):
            pdf.set_font("Helvetica", 'B', 14)
            pdf.cell(0, 10, line.replace("### ", ""), ln=True, border='B')
            pdf.ln(5)
        elif line.startswith("---"):
             pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
             pdf.ln(5)
        elif line.startswith("|"):
            pdf.set_font("Courier", size=9)
            pdf.cell(0, 5, line, ln=True)
        elif line.startswith("```"):
            pdf.set_font("Courier", 'B', 9)
            pdf.set_fill_color(240, 240, 240)
            pdf.multi_cell(0, 5, line.replace("```", "").strip(), border=1, fill=True)
            pdf.ln(2)
        elif line.strip() == "":
            pdf.ln(5)
        else:
            pdf.set_font("Helvetica", size=10)
            # Clean up potential markdown bolding
            line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
            pdf.multi_cell(0, 5, line, ln=True)
    
    return pdf.output(dest='S').encode('latin1')

# --- 3. Streamlit Application UI ---

st.set_page_config(layout="wide")
st.title("🤖 AIOps Incident Report Generator")
st.info(f"This tool analyzes the log file **{LOG_FILE_NAME}** from the MinIO bucket **'{MINIO_BUCKET}'** to generate an incident report.")

if 'report' not in st.session_state:
    st.session_state.report = ""

if st.button("Analyze Latest Incident"):
    st.session_state.report = ""
    
    with st.spinner("Running analysis... Please wait."):
        log_content = read_log_from_minio(MINIO_BUCKET, LOG_FILE_NAME)
        
        if log_content and log_content.strip():
            st.session_state.report = query_model_for_report(log_content)
        elif log_content is not None:
            st.warning(f"Analysis skipped: The log file '{LOG_FILE_NAME}' is empty.")
        else:
            st.error("Failed to retrieve logs. Cannot proceed with analysis.")

if st.session_state.report:
    st.markdown("---")
    st.subheader("Generated Incident Report")
    
    st.markdown(st.session_state.report)

    st.markdown("---")
    st.subheader("Download Report")

    try:
        pdf_bytes = generate_pdf(st.session_state.report)
        st.download_button(
            label="📥 Download as PDF",
            data=pdf_bytes,
            file_name="incident_report.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")

