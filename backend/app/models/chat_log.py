"""
Chat Log Model
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    emotion_log_id = Column(UUID(as_uuid=True), ForeignKey('emotion_logs.id', ondelete='CASCADE'), nullable=True)
    session_id = Column(String(100), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    is_user = Column(Boolean, nullable=False)
    is_crisis = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        role = "User" if self.is_user else "AI"
        return f"<ChatLog {role}: {self.message[:30]}...>"