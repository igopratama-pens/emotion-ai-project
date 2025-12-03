"""
Chat Router
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.chat import ChatRequest, ChatResponse
from ..services.chat_service import ChatService

router = APIRouter(prefix="/api/chat", tags=["AI Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    data: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with AI companion
    
    - **emotion**: Current detected emotion
    - **message**: User message
    - **session_id**: Browser session ID
    - **emotion_log_id**: Related emotion log ID
    - **history**: Previous chat messages
    """
    
    result = await ChatService.chat(
        emotion=data.emotion,
        user_message=data.message,
        session_id=data.session_id,
        emotion_log_id=data.emotion_log_id,
        chat_history=data.history,
        db=db
    )
    
    return result

@router.get("/history/{session_id}")
async def get_chat_history(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get chat history for a session"""
    logs = ChatService.get_chat_history(db, session_id=session_id, limit=limit)
    return {"session_id": session_id, "logs": logs}

@router.get("/crisis")
async def get_crisis_chats(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get chats with crisis detection (admin only)"""
    logs = ChatService.get_crisis_chats(db, limit=limit)
    return {"crisis_chats": logs, "count": len(logs)}