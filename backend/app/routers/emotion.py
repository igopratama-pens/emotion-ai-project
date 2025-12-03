"""
Emotion Detection Router
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.emotion import EmotionDetectRequest, EmotionDetectResponse
from ..services.emotion_service import EmotionService

router = APIRouter(prefix="/api/emotion", tags=["Emotion Detection"])

@router.post("/detect", response_model=EmotionDetectResponse)
async def detect_emotion(
    request: Request,
    data: EmotionDetectRequest,
    db: Session = Depends(get_db)
):
    """
    Detect emotion from image
    
    - **image**: Base64 encoded image
    - **session_id**: Browser session ID
    """
    
    # Get client info
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None
    
    result = EmotionService.detect_emotion(
        image_base64=data.image,
        session_id=data.session_id,
        db=db,
        user_agent=user_agent,
        ip_address=ip_address
    )
    
    return result

@router.get("/stats")
async def get_emotion_stats(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get emotion statistics for last N days"""
    return EmotionService.get_emotion_stats(db, days)

@router.get("/history/{session_id}")
async def get_emotion_history(
    session_id: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get emotion detection history for a session"""
    logs = EmotionService.get_emotion_logs(db, session_id=session_id, limit=limit)
    return {"session_id": session_id, "logs": logs}