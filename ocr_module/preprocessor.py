import os
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image_path, method="basic"):
    """
    Preprocess image for better OCR accuracy
    """
    try:
        if method == "basic":
            return preprocess_basic(image_path)
        elif method == "medical":
            return preprocess_medical_report(image_path)
        else:
            return image_path
    except Exception as e:
        print(f"Preprocessing failed: {e}")
        return image_path

def preprocess_basic(image_path):
    """Basic preprocessing using PIL only"""
    try:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_preprocessed{ext}"
        
        with Image.open(image_path) as img:
            if img.mode != 'L':
                img = img.convert('L')
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            
            img.save(output_path)
            print(f"Basic preprocessing completed: {os.path.basename(output_path)}")
            return output_path
            
    except Exception as e:
        print(f"Basic preprocessing failed: {e}")
        return image_path

def preprocess_medical_report(image_path):
    """Medical report preprocessing using PIL only"""
    try:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_medical{ext}"
        
        with Image.open(image_path) as img:
            if img.mode != 'L':
                img = img.convert('L')
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            
            img = img.filter(ImageFilter.MedianFilter(size=3))
            
            img.save(output_path)
            print(f"Medical preprocessing completed: {os.path.basename(output_path)}")
            return output_path
            
    except Exception as e:
        print(f"Medical preprocessing failed: {e}")
        return image_path
class ImagePreprocessor:
    """
    Simple wrapper class for your existing preprocessing functions
    This is what your medical_ocr_service.py is trying to import
    """
    
    def __init__(self):
        pass
    
    def enhance_image(self, image_path, method="basic"):
        """Use your existing preprocess_image function"""
        return preprocess_image(image_path, method)
    
    def preprocess_medical_document(self, image_path):
        """Use your existing preprocess_medical_report function"""
        return preprocess_medical_report(image_path)