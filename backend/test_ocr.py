from utils.ocr_utils import extract_dob

image_path = "sample-data/aadhaar_sample.jpg"

dob, confidence, age_years, is_18_plus = extract_dob(image_path)

print("\n===== OCR RESULT =====")
print(f"Extracted DOB: {dob}")
print(f"Confidence: {confidence:.2f}")
print(f"Age: {age_years} years")
print(f"Meets 18+ criteria: {'✅ Yes' if is_18_plus else '❌ No'}")
print("======================\n")
