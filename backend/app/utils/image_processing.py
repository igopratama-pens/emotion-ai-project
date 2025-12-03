"""
Image Processing Utilities (Legacy Logic)
"""
import base64
import io
import cv2
import numpy as np
from PIL import Image
from fastapi import HTTPException
from ..config import settings

def decode_base64_image(base64_string: str) -> np.ndarray:
    """
    Decode base64 string to numpy array (BGR)
    """
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        img_bytes = base64.b64decode(base64_string)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img_array = np.array(img)
        
        # Convert RGB (PIL) to BGR (OpenCV)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        return img_bgr
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

def preprocess_for_model(image: np.ndarray, target_size: int = None) -> np.ndarray:
    """
    Preprocess image for CNN model (Matches app_lama logic)
    """
    # Default ke IMG_SIZE dari config (100)
    if target_size is None:
        target_size = settings.IMG_SIZE

    try:
        # 1. Convert BGR to RGB (Model dilatih dengan data RGB)
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # 2. Resize ke 100x100
        img_resized = cv2.resize(img_rgb, (target_size, target_size))
        
        # 3. Normalize [0, 1]
        img_normalized = img_resized.astype('float32') / 255.0
        
        # 4. Expand Dims (Batch)
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image preprocessing error: {str(e)}")