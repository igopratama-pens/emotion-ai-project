"""
Face Detection using MediaPipe (Legacy Accurate Logic + Fixed Color Consistency)
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Tuple

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection

face_detection = mp_face_detection.FaceDetection(
    model_selection=1,              # Sama seperti app_lama (lebih akurat)
    min_detection_confidence=0.5
)


def detect_and_crop_face(image: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    Detect face in image and crop it.
    Input image: BGR
    Output face: BGR (ALWAYS)
    """
    try:
        # Convert BGR → RGB untuk MediaPipe processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        results = face_detection.process(image_rgb)

        if results.detections:
            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box

            h, w = image.shape[:2]

            # Convert relative box ke pixel
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            fw = int(bbox.width * w)
            fh = int(bbox.height * h)

            # --- LEGACY FIX: Margin 20% (persis app_lama) ---
            margin = int(0.2 * min(fw, fh))

            x = max(0, x - margin)
            y = max(0, y - margin)
            fw = min(w - x, fw + 2 * margin)
            fh = min(h - y, fh + 2 * margin)

            # --- 🔥 CRITICAL FIX: Crop dari BGR original, BUKAN RGB ---
            face = image[y:y+fh, x:x+fw]

            if face.size > 0:
                return face, True  # ALWAYS RETURN BGR

        # Fallback: center crop (format tetap BGR)
        return center_crop(image), False

    except Exception as e:
        print(f"[Face Detection Error] {e}")
        return center_crop(image), False


def center_crop(image: np.ndarray) -> np.ndarray:
    """
    Fallback: center crop to square
    Always returns BGR
    """
    h, w = image.shape[:2]
    size = min(h, w)

    start_x = (w - size) // 2
    start_y = (h - size) // 2

    return image[start_y:start_y+size, start_x:start_x+size]