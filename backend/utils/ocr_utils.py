# ocr_utils.py
import torch
import easyocr
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import re
from datetime import datetime

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load TrOCR (printed) model
trocr_model_name = "microsoft/trocr-base-printed"
trocr_model = VisionEncoderDecoderModel.from_pretrained(trocr_model_name).to(device)
trocr_processor = TrOCRProcessor.from_pretrained(trocr_model_name)

# EasyOCR reader
easyocr_reader = easyocr.Reader(['en'], gpu=(device=="cuda"))

# Extract DOB from text
def extract_dob(text):
    # Pattern: dd/mm/yyyy
    match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    if match:
        return match.group(1), 0.95  # High confidence if found
    else:
        return "DOB not found", 0.0

# Compute age
def compute_age(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%d/%m/%Y")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age, age >= 18
    except Exception as e:
        print(f"Error computing age: {e}")
        return 0, False

# Main function
def ocr_extract_info(image_path):
    result = {}
    
    # Load image
    image = Image.open(image_path).convert("RGB")
    
    # Try TrOCR first
    try:
        print("👉 GPU available — trying TrOCR first...")
        pixel_values = trocr_processor(images=image, return_tensors="pt").pixel_values.to(device)
        generated_ids = trocr_model.generate(pixel_values, max_length=512)
        generated_text = trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(f"[TrOCR] Full text: {generated_text}")

        dob_str, confidence = extract_dob(generated_text)
    except Exception as e:
        print(f"[TrOCR] Error: {e}")
        print("👉 Fallback to EasyOCR...")

        # EasyOCR fallback
        try:
            result_easyocr = easyocr_reader.readtext(image_path, detail=0, paragraph=True)
            full_text = " ".join(result_easyocr)
            print(f"[EasyOCR] Full text: {full_text}")

            dob_str, confidence = extract_dob(full_text)
        except Exception as e2:
            print(f"[EasyOCR] Error: {e2}")
            dob_str = "DOB not found"
            confidence = 0.0
    
    # Compute age
    age, is_18_or_more = compute_age(dob_str)
    
    # Final result
    print("\n===== OCR RESULT =====")
    print(f"Extracted DOB: {dob_str}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Age: {age} years")
    print(f"Meets 18+ criteria: {'✅ Yes' if is_18_or_more else '❌ No'}")
    print("======================\n")
    
    result['dob'] = dob_str
    result['confidence'] = round(confidence, 2)
    result['age'] = age
    result['is_18_or_more'] = is_18_or_more
    
    return result
