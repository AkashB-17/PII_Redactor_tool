"""
Streamlit Web UI for PII Redactor
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from src.docx_processor import DocxProcessor
from src.pdf_processor import PdfProcessor

# Ensure output directory exists
os.makedirs("data/output", exist_ok=True)

st.set_page_config(page_title="PII Redaction Tool", layout="centered")

st.title("Automated PII Redaction Tool")
st.write("Upload a DOCX or PDF file to automatically detect and replace sensitive information (PII) with synthetic data.")

# File uploader
uploaded_file = st.file_uploader("Choose a document", type=["docx", "pdf"])

if uploaded_file is not None:
    # Get file extension
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    # Create temporary paths for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_in:
        temp_in.write(uploaded_file.getvalue())
        input_path = temp_in.name
        
    output_filename = f"Redacted_{uploaded_file.name}"
    output_path = os.path.join("data/output", output_filename)

    if st.button("Redact Document"):
        with st.spinner("Analyzing and redacting document..."):
            try:
                # Route to the correct processor based on extension
                if file_extension == ".docx":
                    processor = DocxProcessor()
                    processor.process(input_path, output_path)
                elif file_extension == ".pdf":
                    processor = PdfProcessor()
                    processor.process(input_path, output_path)
                
                st.success(" Redaction Complete!")
                
                # Provide download button
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Redacted Document",
                        data=file,
                        file_name=output_filename,
                        mime="application/octet-stream"
                    )
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
            finally:
                # Cleanup temp input file
                if os.path.exists(input_path):
                    os.remove(input_path)