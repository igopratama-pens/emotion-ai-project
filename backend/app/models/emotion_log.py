"""
Emotion Log Model
"""
from sqlalchemy import Column, String, Float, Boolean, DateTime, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from ..database import Base

class EmotionLog(Base):
    __tablename__ = "emotion_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(100), nullable=False, index=True)
    emotion = Column(String(20), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    all_probabilities = Column(JSONB, nullable=True)
    face_detected = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    __table_args__ = (
        CheckConstraint(
            "emotion IN ('Happiness', 'Sadness', 'Anger', 'Fear', 'Surprise', 'Disgust', 'Neutral')",
            name="valid_emotion"
        ),
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="valid_confidence"
        ),
    )
    
    def __repr__(self):
        return f"<EmotionLog {self.emotion} ({self.confidence:.2f})>"