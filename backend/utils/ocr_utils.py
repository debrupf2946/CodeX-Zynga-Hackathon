import easyocr
import re
from datetime import datetime

def run_easyocr(image_path):
    reader = easyocr.Reader(['en'], gpu=False)  # or gpu=True if you want
    result = reader.readtext(image_path, detail=0)
    full_text = " ".join(result)
    print(f"[EasyOCR] Full text: {full_text}")

    # DOB Extraction using regex
    dob_match = re.search(r'\d{2}/\d{2}/\d{4}', full_text)
    if dob_match:
        dob = dob_match.group(0)
        confidence = 0.85  # EasyOCR doesn't give exact confidence, fixed estimate
    else:
        dob = "DOB not found"
        confidence = 0.00

    try:
        age = compute_age(dob)
        is_18 = age >= 18
    except:
        age = 0
        is_18 = False

    return {
        'dob': dob,
        'confidence': confidence,
        'age': age,
        'is_18_or_more': is_18
    }

def compute_age(dob_str):
    dob = datetime.strptime(dob_str, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def ocr_extract_info(image_path):
    return run_easyocr(image_path)
