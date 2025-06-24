# utils/ocr_utils.py

import easyocr
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import re
import torch

# Device: auto-select GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Initialize EasyOCR reader
easyocr_reader = easyocr.Reader(['en', 'hi'])  # English + Hindi for Aadhaar

# Load TrOCR model + processor
trocr_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
trocr_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
trocr_model = trocr_model.to(device)

# EasyOCR function
def extract_dob_easyocr(image_path):
    try:
        results = easyocr_reader.readtext(image_path)
        full_text = " ".join([text for (_, text, _) in results])

        # Regex
        dob_pattern = r'(\d{2}/\d{2}/\d{4})'
        yob_pattern = r'(Year of Birth|YOB)\s*:?(\d{4})'

        for (bbox, text, prob) in results:
            if re.search(dob_pattern, text):
                return re.search(dob_pattern, text).group(1), prob
            elif re.search(yob_pattern, text):
                return re.search(yob_pattern, text).group(2), prob

    except Exception as e:
        print(f"[EasyOCR] Error: {e}")

    return "DOB not found", 0.0

# TrOCR function
def extract_dob_trocr(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        pixel_values = trocr_processor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        generated_ids = trocr_model.generate(pixel_values)
        generated_text = trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        dob_pattern = r'(\d{2}/\d{2}/\d{4})'
        yob_pattern = r'(Year of Birth|YOB)\s*:?(\d{4})'

        dob_match = re.search(dob_pattern, generated_text)
        if dob_match:
            return dob_match.group(1), 1.0

        yob_match = re.search(yob_pattern, generated_text)
        if yob_match:
            return yob_match.group(2), 1.0

        return "DOB not found", 0.0

    except Exception as e:
        print(f"[TrOCR] Error: {e}")
        return "DOB not found", 0.0

# Final wrapper function

def extract_dob(image_path):
    if device == 'cuda':
        print("👉 GPU available — trying TrOCR first...")
        dob_trocr, conf_trocr = extract_dob_trocr(image_path)
        if dob_trocr != "DOB not found":
            print(f"[TrOCR] DOB: {dob_trocr}, Confidence: {conf_trocr:.2f}")
            return dob_trocr, conf_trocr

        print("👉 Fallback to EasyOCR...")
        dob_easy, conf_easy = extract_dob_easyocr(image_path)
        print(f"[EasyOCR] DOB: {dob_easy}, Confidence: {conf_easy:.2f}")
        return dob_easy, conf_easy

    else:
        print("👉 CPU only — trying EasyOCR first...")
        dob_easy, conf_easy = extract_dob_easyocr(image_path)
        if dob_easy != "DOB not found":
            print(f"[EasyOCR] DOB: {dob_easy}, Confidence: {conf_easy:.2f}")
            return dob_easy, conf_easy

        print("👉 Fallback to TrOCR...")
        dob_trocr, conf_trocr = extract_dob_trocr(image_path)
        print(f"[TrOCR] DOB: {dob_trocr}, Confidence: {conf_trocr:.2f}")
        return dob_trocr, conf_trocr
