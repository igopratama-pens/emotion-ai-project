"""
Chat Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from uuid import UUID

class ChatRequest(BaseModel):
    emotion: str = Field(..., description="Current detected emotion")
    message: str = Field(..., description="User message")
    session_id: str = Field(..., description="Browser session ID")
    emotion_log_id: str = Field(..., description="Related emotion log ID")
    history: List[Dict] = Field(default=[], description="Previous chat history")

class ChatResponse(BaseModel):
    response: str
    emergency: bool = False
    hotlines: Optional[List[str]] = None

class ChatLogResponse(BaseModel):
    id: UUID
    session_id: str
    message: str
    response: str
    is_user: bool
    is_crisis: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True