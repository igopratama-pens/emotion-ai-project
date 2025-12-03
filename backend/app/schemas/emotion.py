"""
Emotion Schemas
"""
from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime
from uuid import UUID

class EmotionDetectRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image")
    session_id: str = Field(..., description="Browser session ID")

class EmotionDetectResponse(BaseModel):
    emotion: str
    confidence: float
    initial_message: str
    all_probabilities: Dict[str, float]
    face_detected: bool
    emotion_log_id: UUID
    
class EmotionLogResponse(BaseModel):
    id: UUID
    session_id: str
    emotion: str
    confidence: float
    face_detected: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True