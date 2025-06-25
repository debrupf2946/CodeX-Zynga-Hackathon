# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.ocr_utils import ocr_extract_info, check_selfie_blur

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

UPLOAD_FOLDER = 'static/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_aadhaar', methods=['POST'])
def upload_aadhaar():
    if 'aadhaar_image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['aadhaar_image']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    result = ocr_extract_info(file_path)

    return jsonify({
        "dob": result['dob'],
        "age_years": result['age'],
        "is_18_plus": result['is_18_or_more'],
        "blurry": result['blurry'],
        "blur_score": result['blur_score'],
        "text": result['text']
    })

@app.route('/api/check_blur', methods=['POST'])
def check_blur():
    if 'selfie' not in request.files:
        return jsonify({"error": "No selfie uploaded"}), 400

    file = request.files['selfie']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    blur_result = check_selfie_blur(file_path)
    return jsonify(blur_result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(host='0.0.0.0', port=port)

