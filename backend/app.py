# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.ocr_utils import ocr_extract_info
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Allow requests from frontend


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



UPLOAD_FOLDER = 'static/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_aadhaar', methods=['POST'])
def upload_aadhaar():
    if 'aadhaar_image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

   file = request.files['aadhaar_image']
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    result = ocr_extract_info(file_path)

    return jsonify({
        "dob": result['dob'],
        "age_years": result['age'],
        "is_18_plus": result['is_18_or_more']
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(host='0.0.0.0', port=port)
