# test_ocr.py

from utils.ocr_utils import extract_dob

# Sample image path — you can put sample aadhaar image here
image_path = "sample-data/aadhaar_sample.jpg"

# Run
dob, confidence = extract_dob(image_path)

# Print result
print(f"Extracted DOB: {dob}")
print(f"Confidence: {confidence:.2f}")
