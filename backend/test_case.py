import cv2
from face_detector import FaceDetector
from face_embedder import FaceEmbedder
from face_comparator import FaceComparator
from face_verification import FaceVerificationSystem

# Initialize paths (update if needed)
ID_PATH = "/Users/apple/ZYNGA_hackathon/Aadhar Card-2.png"
SELFIE_PATH = "/Users/apple/ZYNGA_hackathon/Passport_Photograph.jpeg"

# Load images
id_img = cv2.imread(ID_PATH)
selfie_img = cv2.imread(SELFIE_PATH)

# Initialize all components
detector = FaceDetector("models/deploy.prototxt", "models/res10_300x300_ssd_iter_140000.caffemodel")
embedder = FaceEmbedder()
comparator = FaceComparator(threshold=0.50)
verifier = FaceVerificationSystem(detector, embedder, comparator)

# Run verification
result = verifier.verify_faces(id_img, selfie_img)

# Output
if result['status'] == 'success':
    print("✅ Match Result:")
    print(result['verification'])
else:
    print("❌ Error:", result['error'])
