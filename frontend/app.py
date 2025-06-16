# AIOps Report Downloader - Streamlit Front-End
#
# This application provides a web interface to:
# 1. Connect to MinIO.
# 2. List all available reports in the '/report' bucket.
# 3. Allow users to download any selected report with a single click.

import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# --- 1. Configuration ---

# MinIO Storage Settings - These should match your environment
MINIO_ENDPOINT = "minio-api-aiops.apps.cluster-hdmxf.hdmxf.sandbox689.opentlc.com"
MINIO_ACCESS_KEY = "minio"
MINIO_SECRET_KEY = "minio123"
REPORTS_BUCKET = "report" # The bucket where reports are stored

# --- 2. MinIO Helper Functions ---

# Use Streamlit's caching to avoid reconnecting on every interaction
@st.cache_resource
def get_minio_client():
    """Establishes and returns a connection to the MinIO S3 client."""
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=f"http://{MINIO_ENDPOINT}",
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY
        )
        return s3_client
    except NoCredentialsError:
        st.error("MinIO credentials not found. Please check your configuration.")
        return None
    except Exception as e:
        st.error(f"Failed to connect to MinIO: {e}")
        return None

@st.cache_data(ttl=60) # Cache the list of files for 60 seconds
def list_reports_in_bucket(s3_client, bucket_name):
    """Lists all files in a specified MinIO bucket."""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            # Return a list of filenames
            return [obj['Key'] for obj in response['Contents']]
        else:
            return [] # Return an empty list if the bucket is empty
    except ClientError as e:
        st.error(f"Could not list files. Ensure the bucket '{bucket_name}' exists. Error: {e}")
        return []

def download_report_from_minio(s3_client, bucket_name, object_name):
    """Downloads a report's content from a MinIO bucket."""
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        # Return the content as bytes, which is what the download button needs
        return response['Body'].read()
    except Exception as e:
        st.error(f"Failed to download '{object_name}': {e}")
        return None

# --- 3. Streamlit Application UI ---

st.set_page_config(layout="centered")
st.title("📄 AIOps Report Downloader")
st.write(f"This application lists and provides download links for reports found in the **{REPORTS_BUCKET}** MinIO bucket.")

# Get the MinIO client
s3_client = get_minio_client()

if s3_client:
    # A button to manually refresh the list of reports
    if st.button("🔄 Refresh Report List"):
        # Clear the cache to get a fresh list
        st.cache_data.clear()

    st.markdown("---")
    
    # Get the list of available reports
    available_reports = list_reports_in_bucket(s3_client, REPORTS_BUCKET)

    if available_reports:
        st.subheader("Available Reports")
        # Display each report with a download button
        for report_name in available_reports:
            st.markdown(f"**{report_name}**")
            
            report_content = download_report_from_minio(s3_client, REPORTS_BUCKET, report_name)
            
            if report_content:
                st.download_button(
                    label="📥 Download Report",
                    data=report_content,
                    file_name=report_name,
                    mime="text/plain" # The MIME type for a .txt file
                )
            st.markdown("---")
    else:
        st.info("No reports found in the bucket. Run the AIOps pipeline to generate a report.")
else:
    st.error("Could not connect to MinIO. Please check the application's configuration and network access.")

