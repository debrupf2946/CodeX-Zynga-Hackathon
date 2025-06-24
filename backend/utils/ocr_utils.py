import easyocr
import re

# Initialize EasyOCR reader
reader = easyocr.Reader(['en', 'hi'])  # Aadhaar is usually English + Hindi

def extract_dob_from_aadhaar(image_path):
    # Read text from image
    results = reader.readtext(image_path)

    print("\n--- OCR Results ---")
    for (bbox, text, prob) in results:
        print(f"Text: {text}, Confidence: {prob:.2f}")

    # Combine all text
    full_text = " ".join([text for (_, text, _) in results])
    print("\n--- Full OCR Text ---")
    print(full_text)

    # Regex for DOB: DD/MM/YYYY
    dob_pattern = r'(\d{2}/\d{2}/\d{4})'
    yob_pattern = r'(Year of Birth|YOB)\s*:?(\d{4})'

    dob_match = re.search(dob_pattern, full_text)
    if dob_match:
        return dob_match.group(1)

    yob_match = re.search(yob_pattern, full_text)
    if yob_match:
        return yob_match.group(2)

    return "DOB not found"

