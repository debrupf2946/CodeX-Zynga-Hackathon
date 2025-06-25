# utils/ocr_utils.py

import easyocr
import re
from datetime import datetime
import torch
from pdf2image import convert_from_path
import os

def convert_pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path)
    img_path = pdf_path.replace('.pdf', '.jpg')
    images[0].save(img_path, 'JPEG')
    return img_path
    
def compute_age(dob_str):
    dob = datetime.strptime(dob_str, "%d/%m/%Y")
    today = datetime.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def ocr_extract_info(image_path):
    if image_path.lower().endswith(".pdf"):
        image_path = convert_pdf_to_image(image_path)
    # Aadhaar languages: en, hi, as, bn, gu, kn, ml, mr, or, pa, ta, te, ur
    aadhaar_langs = [
        'en', 'hi', 'as', 'bn', 'gu', 'kn', 'ml', 'mr',
        'or', 'pa', 'ta', 'te', 'ur'
    ]
    # Auto-detect GPU
    gpu_available = torch.cuda.is_available()
    print(f"👉 EasyOCR — using GPU: {gpu_available}")

    reader = easyocr.Reader(aadhaar_langs, gpu=gpu_available)
    result = reader.readtext(image_path, detail=0)
    full_text = " ".join(result)
    print(f"[EasyOCR] Full text: {full_text}")

    # Extract DOB using regex
    dob_match = re.search(r'\d{2}/\d{2}/\d{4}', full_text)
    if dob_match:
        dob = dob_match.group(0)
    else:
        dob = "DOB not found"

    try:
        age_years = compute_age(dob) if dob != "DOB not found" else 0
        is_18_plus = age_years >= 18
    except Exception as e:
        print(f"Error computing age: {e}")
        age_years = 0
        is_18_plus = False

    return {
        'dob': dob,
        'age': age_years,
        'is_18_or_more': is_18_plus
    }
