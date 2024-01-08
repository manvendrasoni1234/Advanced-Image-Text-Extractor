from PIL import Image
import pytesseract
import easyocr
from langdetect import detect
import logging
from colorama import Fore, Style, init
import time
import sys

# Initialize colorama
init(autoreset=True)

class AdvancedImageTextExtractor:
    def __init__(self):
        # Set up logging configuration
        logging.basicConfig(filename='image_text_extractor.log', level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s: %(message)s')

        # Set the paths to the OCR engines
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.easyocr_reader = easyocr.Reader(['en'])

        # Define a simple access control mechanism
        self.allowed_users = {'user1': 'password1', 'user2': 'password2'}

    def authenticate_user(self, username, password):
        return username in self.allowed_users and self.allowed_users[username] == password

    def extract_text_from_image(self, image_path, username, password, language='eng', ocr_engine='tesseract',
                                preprocessing=True, rotation_correction=True, roi_extraction=None):
        try:
            # Authenticate the user
            if not self.authenticate_user(username, password):
                print("Authentication failed.")
                logging.error(f"Authentication failed for user: {username}")
                return None

            # Open the image file
            img = Image.open(image_path)

            # Apply preprocessing
            if preprocessing:
                img = self.preprocess_image(img)

            # Correct rotation
            if rotation_correction:
                img = self.correct_rotation(img)

            # Extract text from ROI if specified
            if roi_extraction:
                img = self.extract_roi(img, roi_extraction)

            # Choose OCR engine based on user preference
            if ocr_engine == 'tesseract':
                extracted_text = pytesseract.image_to_string(img, lang=language)
            elif ocr_engine == 'easyocr':
                extracted_text = ' '.join(self.easyocr_reader.readtext(image_path, detail=0, allowlist='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
            else:
                error_msg = f"Unsupported OCR engine: {ocr_engine}"
                print(error_msg)
                logging.error(error_msg)
                return None

            # Detect the language of the extracted text
            detected_language = detect(extracted_text)

            return {'text': extracted_text.strip(), 'language': detected_language}
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logging.error(error_msg)
            return None

    def preprocess_image(self, img):
        # Apply image preprocessing techniques (e.g., resizing, denoising, thresholding)
        # Add your preprocessing logic here
        return img

    def correct_rotation(self, img):
        # Automatically detect and correct text orientation in rotated images
        # Add your rotation correction logic here
        return img

    def extract_roi(self, img, roi_params):
        # Extract text from a specific Region of Interest (ROI)
        # Add your ROI extraction logic here
        return img

    def batch_process_images(self, image_paths, username, password, language='eng', ocr_engine='tesseract',
                             preprocessing=True, rotation_correction=True, roi_extraction=None):
        results = {}
        for image_path in image_paths:
            result = self.extract_text_from_image(image_path, username, password, language, ocr_engine,
                                                  preprocessing, rotation_correction, roi_extraction)
            results[image_path] = result
        return results

    def print_loading_animation(self):
        sys.stdout.write("\nLoading: [")
        for _ in range(20):
            sys.stdout.write("=")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("] Complete!\n")

    def print_colored_text(self, text, color):
        print(f"{color}{text}{Style.RESET_ALL}")
        
        

# Opening message or ASCII art
opening_message = """
  _______      ________    ___   ___  __        ________     ___  __
   ___   _    _  _____ _____  ________     __  __ ______ _   _ 
 / _ \ | |  | |/ ____|  __ \ |  ____\ \   / / |  |  ____| \ | |
| | | || |  | | (___ | |  | || |__   \ \_/ /  |  | |__  |  \| |
| | | || |  | |\___ \| |  | ||  __|   \   /   |  |  __| | . ` |
| | | || |__| |____) | |__| || |____   | |    |  | |____| |\  |
|_| |_(_)____/|_____/|_____/ |______|  |_|    |__|______|_| \_|


Welcome to the Advanced Image Text Extractor!
Initiating extraction process...
"""

print(opening_message)
time.sleep(2)  # Simulate a brief pause for dramatic effect

# Example usage
image_path = 'img.png'
image_paths_batch = ['img1.png', 'img2.png']

text_extractor = AdvancedImageTextExtractor()

# Print loading animation
text_extractor.print_loading_animation()

# Single image extraction using Tesseract
# Single image extraction using Tesseract
result_single_tesseract = text_extractor.extract_text_from_image(image_path, 'user1', 'password1')
print("\nExtracted Text (Single Image - Tesseract):")
if result_single_tesseract:
    text_extractor.print_colored_text(result_single_tesseract['text'], Fore.GREEN)
    print(f"Detected Language: {result_single_tesseract['language']}")

# Single image extraction using EasyOCR
result_single_easyocr = text_extractor.extract_text_from_image(image_path, 'user1', 'password1', ocr_engine='easyocr')
print("\nExtracted Text (Single Image - EasyOCR):")
if result_single_easyocr:
    text_extractor.print_colored_text(result_single_easyocr['text'], Fore.BLUE)
    print(f"Detected Language: {result_single_easyocr['language']}")

# Batch image extraction using Tesseract
results_batch_tesseract = text_extractor.batch_process_images(image_paths_batch, 'user1', 'password1')
print("\nExtracted Text (Batch Processing - Tesseract):")
for path, result in results_batch_tesseract.items():
    print(f"--- Image: {path} ---")
    text_extractor.print_colored_text(result['text'], Fore.YELLOW)
    print(f"Detected Language: {result['language']}")
print("---------------")

# Batch image extraction using EasyOCR
results_batch_easyocr = text_extractor.batch_process_images(image_paths_batch, 'user1', 'password1', ocr_engine='easyocr')
print("\nExtracted Text (Batch Processing - EasyOCR):")
for path, result in results_batch_easyocr.items():
    print(f"--- Image: {path} ---")
    text_extractor.print_colored_text(result['text'], Fore.YELLOW)
    print(f"Detected Language: {result['language']}")
print("---------------")

# End of the program
text_extractor.print_colored_text("\nExtraction process completed!", Fore.GREEN)
