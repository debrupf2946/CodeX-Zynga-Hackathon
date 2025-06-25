from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
from utils.ocr_utils import ocr_extract_info, convert_pdf_to_image
from backend.face_detector import FaceDetector
from backend.face_embedder import FaceEmbedder
from backend.face_comparator import FaceComparator
from backend.face_verification import FaceVerificationSystem
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load face verification components
face_detector = FaceDetector(
    prototxt_path="models/deploy.prototxt.txt",
    model_path="models/res10_300x300_ssd_iter_140000.caffemodel"
)
face_embedder = FaceEmbedder()
face_comparator = FaceComparator(threshold=0.65)
face_verifier = FaceVerificationSystem(face_detector, face_embedder, face_comparator)

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
    
    # Convert PDF to image if needed
    if file_path.lower().endswith(".pdf"):
        file_path = convert_pdf_to_image(file_path)
    
    result = ocr_extract_info(file_path)

    return jsonify({
        "dob": result['dob'],
        "age_years": result['age'],
        "is_18_plus": result['is_18_or_more']
    })

@app.route('/verify', methods=['POST'])
def verify_faces():
    if 'aadhar' not in request.files or 'selfie' not in request.files:
        return jsonify({"error": "Both Aadhaar and Selfie images are required"}), 400

    aadhar = request.files['aadhar']
    selfie = request.files['selfie']

    if not allowed_file(aadhar.filename) or not allowed_file(selfie.filename):
        return jsonify({"error": "Invalid file format"}), 400

    aadhaar_path = os.path.join(UPLOAD_FOLDER, 'aadhaar.jpg')
    selfie_path = os.path.join(UPLOAD_FOLDER, 'selfie.jpg')
    aadhar.save(aadhaar_path)
    selfie.save(selfie_path)

    ocr_result = ocr_extract_info(aadhaar_path)

    id_image = cv2.imread(aadhaar_path)
    selfie_image = cv2.imread(selfie_path)

    verification = face_verifier.verify_faces(id_image, selfie_image)

    if verification['status'] != 'success':
        return jsonify({"error": verification['error']}), 500

    return jsonify({
        "dob": ocr_result['dob'],
        "age": ocr_result['age'],
        "is18Plus": ocr_result['is_18_or_more'],
        "isMatch": verification['verification']['match'],
        "matchScore": verification['verification']['confidence'],
        "quality": verification['verification']['quality']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
