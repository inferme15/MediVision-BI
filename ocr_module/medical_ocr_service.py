import os
import csv
from datetime import datetime

try:
    from parser import extract_patient_info, extract_test_values
except ImportError:
    def extract_patient_info(text, interactive=False):
        return {'Name': 'Unknown', 'Patient ID': 'Unknown', 'Gender': 'Unknown', 'Age': 'Unknown', 'Test Date': 'Unknown'}

    def extract_test_values(text):
        return [{'Test Name': 'Sample Test', 'Value': '100', 'Unit': 'mg/dL', 'Reference Range': '70-99'}]

try:
    from preprocessor import ImagePreprocessor
except ImportError:
    ImagePreprocessor = None

try:
    from pdf2image import convert_from_path
    PDF_PROCESSING_AVAILABLE = True
except ImportError:
    PDF_PROCESSING_AVAILABLE = False

class MedicalOCRService:
    def __init__(self, poppler_path=None):
        self.poppler_path = poppler_path
        if ImagePreprocessor:
            self.preprocessor = ImagePreprocessor()
        else:
            self.preprocessor = None

    def process_uploaded_file(self, uploaded_file_path, output_dir="./output"):
        start_time = datetime.now()

        try:
            os.makedirs(output_dir, exist_ok=True)
            if not os.path.exists(uploaded_file_path):
                return {'success': False, 'error': f'File not found: {uploaded_file_path}'}

            if not PDF_PROCESSING_AVAILABLE:
                return {'success': False, 'error': 'pdf2image not available'}

            if self.poppler_path:
                images = convert_from_path(uploaded_file_path, poppler_path=self.poppler_path)
            else:
                images = convert_from_path(uploaded_file_path)

            all_text = ""
            for image in images:
                if self.preprocessor:
                    image = self.preprocessor.preprocess(image)
                all_text += self._extract_text_from_image(image) + "\n"

            patient_info = extract_patient_info(all_text)
            test_results = extract_test_values(all_text)

            csv_filename = f"{patient_info.get('Name','Unknown').replace(' ','_')}_{patient_info.get('Patient ID','000')}.csv"
            csv_path = os.path.join(output_dir, csv_filename)
            self._save_to_csv(patient_info, test_results, csv_path)

            processing_time = (datetime.now() - start_time).total_seconds()
            return {
                'success': True,
                'patient_info': patient_info,
                'test_results': test_results,
                'csv_path': csv_path,
                'csv_filename': csv_filename,
                'num_tests': len(test_results),
                'processing_time': processing_time,
                'error': None
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _extract_text_from_image(self, image):
        try:
            import pytesseract
            return pytesseract.image_to_string(image, config='--psm 6')
        except ImportError:
            try:
                import easyocr
                reader = easyocr.Reader(['en'])
                results = reader.readtext(image)
                return ' '.join([result[1] for result in results])
            except ImportError:
                return "OCR not available"

    def _save_to_csv(self, patient_info, test_results, csv_path):
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['PATIENT INFORMATION'])
            for key, value in patient_info.items():
                writer.writerow([key, value])
            writer.writerow([])
            writer.writerow(['TEST RESULTS'])
            writer.writerow(['Test Name', 'Value', 'Unit', 'Reference Range', 'Status'])
            for test in test_results:
                writer.writerow([
                    test.get('Test Name', ''),
                    test.get('Value', ''),
                    test.get('Unit', ''),
                    test.get('Reference Range', ''),
                    test.get('Status', '')
                ])

# This is the function your Streamlit app expects to import
def process_uploaded_pdf(input_path, output_path="data/processed/"):
    service = MedicalOCRService(
        poppler_path=r"C:/Users/prish/Downloads/Release-24.08.0-0/poppler-24.08.0/Library/bin"
    )
    return service.process_uploaded_file(input_path, output_path)
