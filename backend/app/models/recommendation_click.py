"""
Recommendation Click Model
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..database import Base

class RecommendationClick(Base):
    __tablename__ = "recommendation_clicks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    emotion_log_id = Column(UUID(as_uuid=True), ForeignKey('emotion_logs.id', ondelete='CASCADE'), nullable=True)
    session_id = Column(String(100), nullable=False)
    emotion = Column(String(20), nullable=False, index=True)
    recommendation_type = Column(String(20), nullable=False, index=True)
    recommendation_title = Column(String(255), nullable=False)
    clicked_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        CheckConstraint(
            "recommendation_type IN ('music', 'food', 'activity')",
            name="valid_recommendation_type"
        ),
    )
    
    def __repr__(self):
        return f"<RecommendationClick {self.recommendation_type}: {self.recommendation_title}>"