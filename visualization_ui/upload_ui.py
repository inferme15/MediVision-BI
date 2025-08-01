import streamlit as st
import os
import sys
import uuid

# ✅ Add parent directory to Python path so we can import from ocr_module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ocr_module.medical_ocr_service import MedicalOCRService  # ✅ this now works

st.set_page_config(page_title="MediVision PDF Uploader")

st.title("📄 Upload Lab Report PDF")
st.write("Upload a PDF lab report. The system will process it automatically.")

UPLOAD_DIR = "upload"
OUTPUT_DIR = "data/processed"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    # ✅ Save using original filename with UUID to avoid overwriting
    original_filename = os.path.splitext(uploaded_file.name)[0]
    safe_filename = f"{original_filename}_{uuid.uuid4().hex[:6]}.pdf"
    saved_pdf_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(saved_pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"✅ File uploaded: `{saved_pdf_path}`")

    if st.button("Run OCR"):
        st.info("🔄 Processing...")

        ocr = MedicalOCRService(poppler_path=None)

        result = ocr.process_uploaded_file(saved_pdf_path, output_dir=OUTPUT_DIR)

        if result["success"]:
            st.success("✅ OCR completed successfully.")
        else:
            st.error("❌ OCR failed.")
            st.code(result["error"])
