from keras_facenet import FaceNet
import numpy as np
import cv2

class FaceEmbedder:
    def __init__(self):
        self.model = FaceNet()
        self.input_size = (160, 160)

    def preprocess_face(self, image, face_coords):
     (x1, y1, x2, y2) = face_coords
     face = image[y1:y2, x1:x2]
     if face.size == 0:
        raise ValueError("Empty face crop. Check coordinates or detection.")
     face = cv2.resize(face, self.input_size)
     face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
     return face

    def get_embedding(self, face):
        embeddings = self.model.embeddings([face])
        return embeddings[0] / np.linalg.norm(embeddings[0])
