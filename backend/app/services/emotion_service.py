"""
Emotion Detection Service
"""
from sqlalchemy.orm import Session
from ..models.emotion_log import EmotionLog
from ..ml.model_loader import emotion_model
from ..utils.image_processing import decode_base64_image, preprocess_for_model
from ..utils.face_detection import detect_and_crop_face
from ..utils.helpers import get_random_initial_message
from ..config import settings
from typing import Tuple, Dict
import numpy as np

class EmotionService:
    """Service for emotion detection"""
    
    @staticmethod
    def detect_emotion(
        image_base64: str,
        session_id: str,
        db: Session,
        user_agent: str = None,
        ip_address: str = None
    ) -> Dict:
        """
        Detect emotion from image and log to database
        
        Args:
            image_base64: Base64 encoded image
            session_id: Browser session ID
            db: Database session
            user_agent: User agent string
            ip_address: Client IP address
        
        Returns:
            Dictionary with emotion detection results
        """
        
        # Decode image
        image = decode_base64_image(image_base64)
        
        # Detect and crop face
        face, face_detected = detect_and_crop_face(image)
        
        # Preprocess for model
        preprocessed = preprocess_for_model(face)
        
        # Predict emotion
        emotion, confidence, probs = emotion_model.predict(preprocessed)
        
        # Format probabilities
        all_probabilities = {
            settings.EMOTIONS[i]: float(probs[i])
            for i in range(len(settings.EMOTIONS))
        }
        
        # Generate initial message
        initial_message = get_random_initial_message(emotion, confidence, face_detected)
        
        # Save to database
        emotion_log = EmotionLog(
            session_id=session_id,
            emotion=emotion,
            confidence=confidence,
            all_probabilities=all_probabilities,
            face_detected=face_detected,
            user_agent=user_agent,
            ip_address=ip_address
        )
        
        db.add(emotion_log)
        db.commit()
        db.refresh(emotion_log)
        
        return {
            "emotion": emotion,
            "confidence": confidence,
            "initial_message": initial_message,
            "all_probabilities": all_probabilities,
            "face_detected": face_detected,
            "emotion_log_id": emotion_log.id
        }
    
    @staticmethod
    def get_emotion_logs(
        db: Session,
        session_id: str = None,
        limit: int = 100,
        offset: int = 0
    ):
        """Get emotion logs"""
        query = db.query(EmotionLog)
        
        if session_id:
            query = query.filter(EmotionLog.session_id == session_id)
        
        return query.order_by(EmotionLog.timestamp.desc()).offset(offset).limit(limit).all()
    
    @staticmethod
    def get_emotion_stats(db: Session, days: int = 7) -> Dict:
        """Get emotion statistics"""
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Count by emotion
        emotion_counts = db.query(
            EmotionLog.emotion,
            func.count(EmotionLog.id).label('count')
        ).filter(
            EmotionLog.timestamp >= start_date
        ).group_by(EmotionLog.emotion).all()
        
        # Average confidence
        avg_confidence = db.query(
            func.avg(EmotionLog.confidence)
        ).filter(
            EmotionLog.timestamp >= start_date
        ).scalar()
        
        # Total detections
        total = db.query(func.count(EmotionLog.id)).filter(
            EmotionLog.timestamp >= start_date
        ).scalar()
        
        return {
            "emotion_counts": {e: c for e, c in emotion_counts},
            "total_detections": total or 0,
            "avg_confidence": float(avg_confidence or 0),
            "days": days
        }