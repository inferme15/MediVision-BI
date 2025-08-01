import streamlit as st
import os
import subprocess

st.set_page_config(page_title="MediVision PDF Uploader")

st.title("📄 Upload Lab Report PDF")
st.write("This uploads a lab report PDF, runs OCR, and generates structured CSV data.")
upload_path = "uploads"
os.makedirs(upload_path, exist_ok=True)

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    saved_file_path = os.path.join(upload_path, "lab_report.pdf")
# Save uploaded PDF to disk
with open(saved_file_path, "wb") as f:
    f.write(uploaded_file.read())

st.success(f"✅ PDF uploaded successfully to {saved_file_path}")

# Trigger the OCR Python script
st.info("🔄 Running OCR to extract lab data...")

from ocr_module.ocr_main import process_uploaded_pdf
# Run the OCR process and capture the result
result = subprocess.run(
    ["python", "-m", "ocr_module.ocr_main", saved_file_path],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    st.success("✅ OCR completed successfully!")
    output_path = "data/processed/sample_output.csv"
    if os.path.exists(output_path):
        st.download_button("Download Extracted CSV", open(output_path, "rb"), file_name="output.csv")
        st.info("You can now run the backend insert_data.py or open Power BI.")
    else:
        st.warning("⚠️ OCR ran, but no output CSV was found.")
else:
    st.error("❌ OCR script failed. Check your console for details.")
    st.code(result.stderr)
