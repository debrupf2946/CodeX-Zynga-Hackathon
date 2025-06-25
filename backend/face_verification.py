from typing import Dict
import numpy as np
import logging

class FaceVerificationSystem:
    def __init__(self, detector, embedder, comparator):
        self.detector = detector
        self.embedder = embedder
        self.comparator = comparator
        self.logger = logging.getLogger(__name__)

    def verify_faces(self, id_image: np.ndarray, selfie_image: np.ndarray) -> Dict:
        result = {
            'status': 'failed',
            'error': None,
            'verification': None,
            'diagnostics': {
                'face_detected_id': False,
                'face_detected_selfie': False
            }
        }

        try:
            id_face = self.detector.detect_largest_face(id_image)
            selfie_face = self.detector.detect_largest_face(selfie_image)

            if not id_face or not selfie_face:
                result['error'] = 'Face detection failed.'
                result['diagnostics'].update({
                    'face_detected_id': bool(id_face),
                    'face_detected_selfie': bool(selfie_face)
                })
                return result

            id_quality = self.detector.get_face_quality(id_image, id_face)
            selfie_quality = self.detector.get_face_quality(selfie_image, selfie_face)

            id_embedding = self.embedder.get_embedding(self.embedder.preprocess_face(id_image, id_face))
            selfie_embedding = self.embedder.get_embedding(self.embedder.preprocess_face(selfie_image, selfie_face))

            _, similarity = self.comparator.compare_embeddings(id_embedding, selfie_embedding)

            result.update({
                'status': 'success',
                'verification': self.comparator.generate_verification_report(
                    similarity, id_quality, selfie_quality),
                'diagnostics': {
                    'face_detected_id': True,
                    'face_detected_selfie': True,
                    'embedding_generated': True
                }
            })
        except Exception as e:
            self.logger.error(f"Verification failed: {str(e)}")
            result['error'] = str(e)

        return result
