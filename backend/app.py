# app.py
from flask import Flask, request, jsonify
import os
from utils.ocr_utils import extract_dob_from_aadhaar
from utils.face_utils import compare_faces

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_aadhaar', methods=['POST'])
def upload_aadhaar():
    file = request.files['aadhaar_image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    dob, confidence, age_years, is_18_plus = extract_dob(image_path)
    return jsonify({
        "dob": dob,
        "confidence": confidence,
        "age_years": age_years,
        "is_18_plus": is_18_plus
    })


if __name__ == '__main__':
    app.run(debug=True)

