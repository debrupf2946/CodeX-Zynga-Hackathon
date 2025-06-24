# test_ocr.py

from utils.ocr_utils import extract_dob

# Sample image path — you can put sample aadhaar image here
image_path = "sample-data/aadhaar_sample.jpg"

# Run
dob = extract_dob(image_path)

# Print result
print(f"\nExtracted DOB: {dob}")
