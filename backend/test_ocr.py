# test_ocr.py

from utils.ocr_utils import ocr_extract_info

# Image uploaded in Colab (name accordingly)
image_path = "sample_data/aadhaar_sample.jpg"

result = ocr_extract_info(image_path)

print("\n===== OCR RESULT =====")
print(f"Extracted DOB: {result['dob']}")
print(f"Age: {result['age']} years")
print(f"Meets 18+ criteria: {'✅ Yes' if result['is_18_or_more'] else '❌ No'}")
print("======================\n")
