# utils/ocr_utils.py

import easyocr
import re
from datetime import datetime
import torch

def compute_age(dob_str):
    dob = datetime.strptime(dob_str, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def ocr_extract_info(image_path):
    # Auto-detect GPU
    gpu_available = torch.cuda.is_available()
    print(f"👉 EasyOCR — using GPU: {gpu_available}")

    reader = easyocr.Reader(['en'], gpu=gpu_available)
    result = reader.readtext(image_path, detail=0)
    full_text = " ".join(result)
    print(f"[EasyOCR] Full text: {full_text}")

    # Extract DOB using regex
    dob_match = re.search(r'\d{2}/\d{2}/\d{4}', full_text)
    if dob_match:
        dob = dob_match.group(0)
        confidence = 0.85  # Estimated confidence
    else:
        dob = "DOB not found"
        confidence = 0.00

    try:
        age_years = compute_age(dob) if dob != "DOB not found" else 0
        is_18_plus = age_years >= 18
    except Exception as e:
        print(f"Error computing age: {e}")
        age_years = 0
        is_18_plus = False

    return {
        'dob': dob,
        'confidence': confidence,
        'age': age_years,
        'is_18_or_more': is_18_plus
    }
