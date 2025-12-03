"""
ML Model Loader - Weight Injection Strategy
"""
import os
import numpy as np
from ..config import settings
from .model_architecture import build_emotion_cnn

class EmotionModel:
    """Singleton class for emotion detection model"""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmotionModel, cls).__new__(cls)
        return cls._instance
    
    def load_model(self):
        """
        Load model using Architecture Reconstruction strategy 
        to bypass 'batch_shape' config error in old h5 files.
        """
        if self._model is None:
            model_path = settings.MODEL_PATH
            
            if not os.path.exists(model_path):
                # Fallback: Coba cari emotion_cnn.h5 jika _fixed tidak ada
                fallback_path = model_path.replace("_fixed.h5", ".h5")
                if os.path.exists(fallback_path):
                    print(f"⚠️ Model fixed not found, switching to: {fallback_path}")
                    model_path = fallback_path
                else:
                    raise FileNotFoundError(f"Model not found at {model_path}")
            
            print(f"🔧 Loading emotion model from {model_path}...")
            print("   Strategy: Rebuild Architecture + Load Weights")
            
            try:
                # 1. Bangun ulang arsitektur bersih dari kode Python
                self._model = build_emotion_cnn()
                
                # 2. Inject bobot dari file h5 (mengabaikan config yang rusak)
                # by_name=True & skip_mismatch=True membuat loading lebih fleksibel
                self._model.load_weights(model_path, by_name=True, skip_mismatch=True)
                
                # 3. Compile (Agar siap prediksi)
                self._model.compile(
                    optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy']
                )
                
                print(f"✓ Model loaded successfully!")
                print(f"   Input: {self._model.input_shape}")
                print(f"   Output: {self._model.output_shape}")
                
            except Exception as e:
                print(f"❌ CRITICAL ERROR loading model: {e}")
                # Jika gagal total, raise error agar ketahuan
                raise e
        
        return self._model
    
    def predict(self, image_array: np.ndarray):
        """
        Predict emotion from image
        """
        if self._model is None:
            self.load_model()
        
        # Predict
        predictions = self._model.predict(image_array, verbose=0)
        probs = predictions[0]
        
        # Get predicted class
        predicted_class = np.argmax(probs)
        confidence = float(probs[predicted_class])
        
        # Get emotion label
        emotion = settings.EMOTIONS[predicted_class]
        
        return emotion, confidence, probs
    
    @property
    def is_loaded(self) -> bool:
        return self._model is not None

# Global instance
emotion_model = EmotionModel()