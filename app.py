"""
Streamlit Web UI for PII Redactor
"""

import os
import tempfile
from pathlib import Path

import streamlit as st

from src.docx_processor import DocxProcessor
from src.pdf_processor import PdfProcessor

os.makedirs("data/output", exist_ok=True)

st.set_page_config(
    page_title="PII Redaction Tool",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Custom styling
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main .block-container {
            padding-top: 2.5rem;
            max-width: 780px;
        }
        h1 {
            font-weight: 700 !important;
        }
        .subtitle {
            color: rgba(120, 120, 120, 0.9);
            font-size: 1.05rem;
            margin-top: -0.6rem;
            margin-bottom: 1.8rem;
        }
        .stat-card {
            background: rgba(120, 120, 120, 0.08);
            border: 1px solid rgba(120, 120, 120, 0.18);
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            text-align: center;
        }
        .stat-number {
            font-size: 1.6rem;
            font-weight: 700;
        }
        .stat-label {
            font-size: 0.8rem;
            color: rgba(120, 120, 120, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        div[data-testid="stFileUploaderDropzone"] {
            border-radius: 12px;
        }
        .footer-note {
            color: rgba(120, 120, 120, 0.7);
            font-size: 0.8rem;
            text-align: center;
            margin-top: 2.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("###  PII Redaction Tool")
    st.markdown(
        "Hybrid **regex + spaCy NER** detection with consistent, "
        "Faker-generated fake replacements."
    )
    st.markdown("---")
    st.markdown("**Detects**")
    st.markdown(
        "- Full names & companies\n"
        "- Emails & phone numbers\n"
        "- SSN / PAN / Aadhaar\n"
        "- Credit card numbers\n"
        "- Dates of birth\n"
        "- IPv4 addresses"
    )
    st.markdown("---")
    st.caption(
        "Files are processed in memory / temp storage only and are not "
        "retained after your session ends."
    )

# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.title(" PII Redaction Tool")
st.markdown(
    '<div class="subtitle">Upload a document, get back a version with every '
    "name, email, phone number, and other sensitive detail replaced by "
    "realistic fake data.</div>",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Upload
# ----------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "Drop a DOCX or PDF here, or click to browse",
    type=["docx", "pdf"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    file_extension = Path(uploaded_file.name).suffix.lower()
    file_size_kb = len(uploaded_file.getvalue()) / 1024

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{uploaded_file.name}**")
        st.caption(f"{file_size_kb:,.0f} KB · {file_extension.upper().lstrip('.')}")
    with col2:
        redact_clicked = st.button("Redact Document", type="primary", use_container_width=True)

    if redact_clicked:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_in:
            temp_in.write(uploaded_file.getvalue())
            input_path = temp_in.name

        output_filename = f"Redacted_{uploaded_file.name}"
        output_path = os.path.join("data/output", output_filename)

        try:
            with st.spinner("Scanning for PII and generating replacements..."):
                if file_extension == ".docx":
                    processor = DocxProcessor()
                    stats = processor.process(input_path, output_path)
                elif file_extension == ".pdf":
                    processor = PdfProcessor()
                    stats = processor.process(input_path, output_path) or {}
                else:
                    stats = {}

            st.success("Redaction complete.")

            total = sum(stats.values())
            if total:
                st.markdown("#### Summary")
                cols = st.columns(min(len(stats), 4) or 1)
                for i, (entity_type, count) in enumerate(
                    sorted(stats.items(), key=lambda kv: kv[1], reverse=True)
                ):
                    with cols[i % len(cols)]:
                        st.markdown(
                            f'<div class="stat-card">'
                            f'<div class="stat-number">{count}</div>'
                            f'<div class="stat-label">{entity_type}</div>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                st.caption(f"{total} total instance(s) redacted across the document.")
            else:
                st.info("No PII was detected in this document.")

            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇ Download Redacted Document",
                    data=f,
                    file_name=output_filename,
                    mime="application/octet-stream",
                    type="primary",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"Something went wrong during processing: {e}")
        finally:
            if os.path.exists(input_path):
                os.remove(input_path)

st.markdown(
    '<div class="footer-note">Built with spaCy, Faker, and Streamlit · '
    "for evaluation and educational use</div>",
    unsafe_allow_html=True,
)