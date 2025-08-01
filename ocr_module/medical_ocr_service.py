# # =============================================================================
# # MEDICAL OCR SERVICE MODULE (medical_ocr_service.py)
# # Team Integration Module - Give this to Member 2
# # Place this file in: ocr_module/medical_ocr_service.py
# # =============================================================================

# import os
# import sys
# import json
# import csv
# from datetime import datetime
# import tempfile
# import shutil

# # Import your existing modules (same folder)
# try:
#     from parser import extract_patient_info, extract_test_values, debug_extraction
#     print("Successfully imported parser functions")
# except ImportError as e:
#     print(f"Could not import from parser: {e}")
#     def extract_patient_info(text, interactive=False):
#         return {'Name': 'Unknown', 'Patient ID': 'Unknown', 'Gender': 'Unknown', 'Age': 'Unknown', 'Test Date': 'Unknown'}
    
#     def extract_test_values(text):
#         return [{'Test Name': 'Sample Test', 'Value': '100', 'Unit': 'mg/dL', 'Reference Range': '70-99'}]

# try:
#     from preprocessor import ImagePreprocessor
#     print("Successfully imported ImagePreprocessor")
# except ImportError as e:
#     print(f"Could not import ImagePreprocessor: {e}")
#     ImagePreprocessor = None

# # For PDF processing, we'll need to handle this differently since you don't have a PDFParser class
# try:
#     import pdf2image
#     from pdf2image import convert_from_path
#     print("PDF2Image available for PDF processing")
#     PDF_PROCESSING_AVAILABLE = True
# except ImportError:
#     print("PDF2Image not available - install with: pip install pdf2image")
#     PDF_PROCESSING_AVAILABLE = False

# class MedicalOCRService:
#     """
#     Medical OCR Service for team integration
#     Member 2 will use this class to process uploaded PDF files
#     """
    
#     def __init__(self, poppler_path=None):
#         """
#         Initialize the OCR service
        
#         Args:
#             poppler_path (str): Path to poppler binaries (required on Windows)
#         """
#         self.poppler_path = poppler_path
        
#         # Initialize image preprocessor if available
#         try:
#             if ImagePreprocessor:
#                 self.preprocessor = ImagePreprocessor()
#                 print("ImagePreprocessor initialized")
#             else:
#                 self.preprocessor = None
#                 print("ImagePreprocessor not available")
#         except Exception as e:
#             self.preprocessor = None
#             print(f"Could not initialize ImagePreprocessor: {e}")
            
#         # Check PDF processing availability
#         if not PDF_PROCESSING_AVAILABLE:
#             print("PDF processing not available. Install pdf2image: pip install pdf2image")
#         else:
#             print("PDF processing ready")
        
#     def process_uploaded_file(self, uploaded_file_path, output_dir="./output"):
#         """
#         Main function for Member 2 to process uploaded PDF files
        
#         Args:
#             uploaded_file_path (str): Path to the uploaded PDF file
#             output_dir (str): Directory to save CSV output
            
#         Returns:
#             dict: Processing results with patient info, test results, and CSV path
#         """
#         start_time = datetime.now()
        
#         try:
#             # Create output directory if it doesn't exist
#             os.makedirs(output_dir, exist_ok=True)
            
#             # Check if file exists
#             if not os.path.exists(uploaded_file_path):
#                 return {
#                     'success': False,
#                     'error': f'File not found: {uploaded_file_path}',
#                     'patient_info': None,
#                     'test_results': None,
#                     'csv_path': None,
#                     'csv_filename': None,
#                     'num_tests': 0,
#                     'processing_time': 0
#                 }
            
#             # Extract images from PDF using pdf2image
#             print(f"Processing PDF: {uploaded_file_path}")
            
#             if not PDF_PROCESSING_AVAILABLE:
#                 return {
#                     'success': False,
#                     'error': 'PDF processing not available. Install pdf2image: pip install pdf2image',
#                     'patient_info': None,
#                     'test_results': None,
#                     'csv_path': None,
#                     'csv_filename': None,
#                     'num_tests': 0,
#                     'processing_time': 0
#                 }
            
#             # Convert PDF to images
#             try:
#                 if self.poppler_path:
#                     images = convert_from_path(uploaded_file_path, poppler_path=self.poppler_path)
#                 else:
#                     images = convert_from_path(uploaded_file_path)
#                 print(f"Extracted {len(images)} pages from PDF")
#             except Exception as e:
#                 return {
#                     'success': False,
#                     'error': f'Could not convert PDF to images: {str(e)}',
#                     'patient_info': None,
#                     'test_results': None,
#                     'csv_path': None,
#                     'csv_filename': None,
#                     'num_tests': 0,
#                     'processing_time': 0
#                 }
            
#             if not images:
#                 return {
#                     'success': False,
#                     'error': 'No images could be extracted from PDF',
#                     'patient_info': None,
#                     'test_results': None,
#                     'csv_path': None,
#                     'csv_filename': None,
#                     'num_tests': 0,
#                     'processing_time': 0
#                 }
            
#             # Process each image and extract text
#             all_text = ""
#             for i, image in enumerate(images):
#                 print(f"Processing page {i+1}/{len(images)}")
                
#                 # Preprocess image
#                 processed_image = self.preprocessor.preprocess(image)
                
#                 # Extract text using OCR
#                 page_text = self._extract_text_from_image(processed_image)
#                 all_text += page_text + "\n"
            
#             # Extract patient information using your parser functions
#             patient_info = extract_patient_info(all_text, interactive=False)
            
#             # Extract test results using your parser functions
#             test_results = extract_test_values(all_text)
            
#             # Generate CSV filename
#             patient_name = patient_info.get('Name', 'Unknown').replace(' ', '_')
#             patient_id = patient_info.get('Patient ID', 'Unknown')
#             timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#             csv_filename = f"{patient_name}_{patient_id}_{timestamp}.csv"
#             csv_path = os.path.join(output_dir, csv_filename)
            
#             # Save to CSV
#             self._save_to_csv(patient_info, test_results, csv_path)
            
#             # Calculate processing time
#             processing_time = (datetime.now() - start_time).total_seconds()
            
#             return {
#                 'success': True,
#                 'patient_info': patient_info,
#                 'test_results': test_results,
#                 'csv_path': csv_path,
#                 'csv_filename': csv_filename,
#                 'num_tests': len(test_results),
#                 'processing_time': processing_time,
#                 'error': None
#             }
            
#         except Exception as e:
#             processing_time = (datetime.now() - start_time).total_seconds()
#             return {
#                 'success': False,
#                 'error': str(e),
#                 'patient_info': None,
#                 'test_results': None,
#                 'csv_path': None,
#                 'csv_filename': None,
#                 'num_tests': 0,
#                 'processing_time': processing_time
#             }
    
#     def process_multiple_files(self, file_paths, output_dir="./output"):
#         """
#         Process multiple PDF files (batch processing)
        
#         Args:
#             file_paths (list): List of PDF file paths
#             output_dir (str): Directory to save CSV outputs
            
#         Returns:
#             list: List of processing results for each file
#         """
#         results = []
        
#         for file_path in file_paths:
#             print(f"\nProcessing file: {os.path.basename(file_path)}")
            
#             result = self.process_uploaded_file(file_path, output_dir)
#             result['original_filename'] = os.path.basename(file_path)
            
#             results.append(result)
        
#         return results
    
#     def _extract_text_from_image(self, image):
#         """
#         Extract text from image using OCR
#         Replace this with your actual OCR implementation
#         """
#         try:
#             # Option 1: If using Tesseract
#             import pytesseract
#             text = pytesseract.image_to_string(image, config='--psm 6')
#             return text
            
#         except ImportError:
#             try:
#                 # Option 2: If using EasyOCR
#                 import easyocr
#                 reader = easyocr.Reader(['en'])
#                 results = reader.readtext(image)
#                 text = ' '.join([result[1] for result in results])
#                 return text
                
#             except ImportError:
#                 # Option 3: Use your existing OCR method
#                 # Replace this with your actual OCR implementation
#                 print("Warning: No OCR library found. Please implement OCR method.")
#                 return "OCR implementation needed"
    
#     def _save_to_csv(self, patient_info, test_results, csv_path):
#         """
#         Save extracted data to CSV file
        
#         Args:
#             patient_info (dict): Patient information
#             test_results (list): List of test results
#             csv_path (str): Path to save CSV file
#         """
#         try:
#             with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
#                 writer = csv.writer(csvfile)
                
#                 # Write patient information header
#                 writer.writerow(['PATIENT INFORMATION'])
#                 for key, value in patient_info.items():
#                     writer.writerow([key, value])
                
#                 # Write empty row
#                 writer.writerow([])
                
#                 # Write test results header
#                 writer.writerow(['TEST RESULTS'])
#                 writer.writerow(['Test Name', 'Value', 'Unit', 'Reference Range', 'Status'])
                
#                 # Write test results
#                 for test in test_results:
#                     writer.writerow([
#                         test.get('Test Name', ''),
#                         test.get('Value', ''),
#                         test.get('Unit', ''),
#                         test.get('Reference Range', ''),
#                         test.get('Status', '')
#                     ])
                
#             print(f"CSV saved: {csv_path}")
            
#         except Exception as e:
#             print(f"Error saving CSV: {str(e)}")
#             raise

#     def get_service_info(self):
#         """
#         Return service information for debugging
#         """
#         return {
#             'service_name': 'MedicalOCRService',
#             'version': '1.0',
#             'poppler_path': self.poppler_path,
#             'status': 'ready'
#         }

# # Example usage for Member 2 (to verification or testing ,use the above code to integrate into your module) this code is to simply check its working or not
# if __name__ == "__main__":
#     # This shows Member 2 how to use your module
    
#     # Initialize OCR service
#     poppler_path = r"C:/Users/GEETHA/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
#     ocr_service = MedicalOCRService(poppler_path=poppler_path)
    
#     # Test with sample file
#     test_file = "../sample_reports/Jane_Smith_Lab_Report.pdf"
    
#     if os.path.exists(test_file):
#         result = ocr_service.process_uploaded_file(
#             uploaded_file_path=test_file,
#             output_dir="../output"
#         )
        
#         if result['success']:
#             print("Processing successful!")
#             print(f"Patient: {result['patient_info']['Name']}")
#             print(f"Tests: {result['num_tests']}")
#             print(f"CSV: {result['csv_filename']}")
#         else:
#             print(f"Processing failed: {result['error']}")
#     else:
#         print(f"Test file not found: {test_file}")

