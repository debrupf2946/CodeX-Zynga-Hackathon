# ocr_utils.py

import re
from datetime import datetime
import torch
from transformers import VisionEncoderDecoderModel, DonutProcessor
import easyocr
from PIL import Image

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load Donut model
donut_model_name = "naver-clova-ix/donut-base-finetuned-cord-v2"
donut_processor = DonutProcessor.from_pretrained(donut_model_name)
donut_model = VisionEncoderDecoderModel.from_pretrained(donut_model_name).to(device)

# Load EasyOCR
easyocr_reader = easyocr.Reader(['en'], gpu=False)

# Helper: compute age
def compute_age(dob_str):
    try:
        if len(dob_str) == 4:
            # Year of birth
            birth_year = int(dob_str)
            birth_date = datetime(birth_year, 1, 1)
        else:
            birth_date = datetime.strptime(dob_str, "%d/%m/%Y")

        today = datetime.today()
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age_years
    except Exception as e:
        print(f"Error computing age: {e}")
        return 0

# Extract DOB with Donut

def extract_dob_donut(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        pixel_values = donut_processor(images=image, return_tensors="pt").pixel_values.to(device)

        # Safe execution: disable AMP autocast
        with torch.cuda.amp.autocast(enabled=False):
            generated_ids = donut_model.generate(pixel_values, max_length=512)

        generated_text = donut_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        print(f"[Donut] Generated text: {generated_text}")

        # Patterns
        dob_pattern = r'(\d{2}/\d{2}/\d{4})'
        yob_pattern = r'(Year of Birth|YOB)[\s:]*?(\d{4})'

        dob_match = re.search(dob_pattern, generated_text)
        if dob_match:
            return dob_match.group(1), 0.98

        yob_match = re.search(yob_pattern, generated_text)
        if yob_match:
            return yob_match.group(2), 0.95

        return "DOB not found", 0.0

    except Exception as e:
        print(f"[Donut] Error: {e}")
        torch.cuda.empty_cache()  # Clean GPU
        return "DOB not found", 0.0

# Extract DOB with EasyOCR
def extract_dob_easyocr(image_path):
    try:
        results = easyocr_reader.readtext(image_path)
        full_text = " ".join([text for (_, text, _) in results])
        print(f"[EasyOCR] Full text: {full_text}")

        dob_pattern = r'(\d{2}/\d{2}/\d{4})'
        yob_pattern = r'(Year of Birth|YOB)[\s:]*?(\d{4})'

        for (bbox, text, prob) in results:
            if re.search(dob_pattern, text):
                return re.search(dob_pattern, text).group(1), prob
            elif re.search(yob_pattern, text):
                return re.search(yob_pattern, text).group(2), prob

        return "DOB not found", 0.0

    except Exception as e:
        print(f"[EasyOCR] Error: {e}")
        return "DOB not found", 0.0

# Main wrapper
def extract_dob(image_path):
    if device == 'cuda':
        print("👉 GPU available — trying Donut first...")
        dob, conf = extract_dob_donut(image_path)
        if dob != "DOB not found":
            age_years = compute_age(dob)
            is_18_plus = age_years >= 18
            print(f"[Donut] DOB: {dob}, Age: {age_years}, 18+: {is_18_plus}, Confidence: {conf:.2f}")
            return dob, conf, age_years, is_18_plus

    print("👉 Fallback to EasyOCR...")
    dob, conf = extract_dob_easyocr(image_path)
    age_years = compute_age(dob)
    is_18_plus = age_years >= 18
    print(f"[EasyOCR] DOB: {dob}, Age: {age_years}, 18+: {is_18_plus}, Confidence: {conf:.2f}")
    return dob, conf, age_years, is_18_plus
