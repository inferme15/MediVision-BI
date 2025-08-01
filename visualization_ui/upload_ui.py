# import streamlit as st
# import os
# import tempfile
# import sys

# # ✅ Add parent directory to Python path so we can import from ocr_module
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from ocr_module.medical_ocr_service import MedicalOCRService  # ✅ this now works

# st.set_page_config(page_title="MediVision PDF Uploader")

# st.title("📄 Upload Lab Report PDF")
# st.write("Upload a PDF lab report, extract data via OCR, and download the structured CSV.")

# UPLOAD_DIR = "upload"
# OUTPUT_DIR = "data/processed"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# if uploaded_file is not None:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=UPLOAD_DIR) as tmp:
#         tmp.write(uploaded_file.read())
#         saved_pdf_path = tmp.name

#     st.success(f"✅ File uploaded: `{saved_pdf_path}`")

#     if st.button("Run OCR"):
#         st.info("🔄 Processing...")

#         ocr = MedicalOCRService(poppler_path=None)

#         result = ocr.process_uploaded_file(saved_pdf_path, output_dir=OUTPUT_DIR)

#         if result["success"]:
#             st.success("✅ OCR completed!")

#             st.subheader("👤 Patient Info")
#             for key, value in result["patient_info"].items():
#                 st.write(f"**{key}:** {value}")

#             st.subheader("📊 Test Results")
#             st.dataframe(result["test_results"])

#             st.subheader("📁 Download CSV")
#             with open(result["csv_path"], "rb") as f:
#                 st.download_button(
#                     label="Download Extracted CSV",
#                     data=f,
#                     file_name=result["csv_filename"],
#                     mime="text/csv"
#                 )
#         else:
#             st.error("❌ OCR failed.")
#             st.code(result["error"])
import streamlit as st
import os
import tempfile
import sys

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", dir=UPLOAD_DIR) as tmp:
        tmp.write(uploaded_file.read())
        saved_pdf_path = tmp.name

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
