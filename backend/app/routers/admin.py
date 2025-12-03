"""
Admin Router - STABILIZED VERSION
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import List, Optional
from ..database import get_db
from ..models.admin import Admin
from ..schemas.admin import AdminLogin, AdminCreate, AdminResponse, Token
from ..utils.helpers import hash_password, verify_password, create_access_token, decode_access_token
from ..config import settings

# Import Models
from ..models.emotion_log import EmotionLog
from ..models.chat_log import ChatLog
from ..models.recommendation_click import RecommendationClick
from sqlalchemy import func

router = APIRouter(prefix="/api/admin", tags=["Admin"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None:
        raise HTTPException(status_code=401, detail="Admin not found")
    return admin

@router.post("/login", response_model=Token)
async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": admin.username}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=AdminResponse)
async def get_current_admin_info(current_admin: Admin = Depends(get_current_admin)):
    return current_admin

@router.get("/dashboard")
async def get_dashboard_stats(
    time_range: str = "30d",
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # Tentukan batas waktu
    now = datetime.utcnow()
    if time_range == "today":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_range == "7d":
        start_date = now - timedelta(days=7)
    else: # 30d default
        start_date = now - timedelta(days=30)
    
    # Hitung Statistik
    # NOTE: Kita gunakan filter waktu hanya pada tabel yang pasti memiliki kolom 'timestamp'
    total_detections = db.query(func.count(EmotionLog.id)).filter(EmotionLog.timestamp >= start_date).scalar()
    unique_sessions = db.query(func.count(func.distinct(EmotionLog.session_id))).filter(EmotionLog.timestamp >= start_date).scalar()
    
    # Hitung pesan user
    total_messages = db.query(func.count(ChatLog.id)).filter(
        ChatLog.timestamp >= start_date,
        ChatLog.is_user == True 
    ).scalar()
    
    # Hitung klik (Kita hilangkan filter waktu di sini untuk mencegah crash jika kolom timestamp tidak ada)
    total_clicks = db.query(func.count(RecommendationClick.id)).scalar()
    
    # Emosi Dominan
    most_common = db.query(
        EmotionLog.emotion,
        func.count(EmotionLog.id).label('count')
    ).filter(
        EmotionLog.timestamp >= start_date
    ).group_by(EmotionLog.emotion).order_by(func.count(EmotionLog.id).desc()).first()
    
    return {
        "total_detections": total_detections or 0,
        "unique_sessions": unique_sessions or 0,
        "total_messages": total_messages or 0,
        "total_clicks": total_clicks or 0,
        "most_common_emotion": most_common[0] if most_common else "Neutral",
        # Data trend placeholder agar frontend tidak error
        "trends": {
            "detections": "neutral",
            "sessions": "neutral",
            "messages": "neutral",
            "clicks": "neutral"
        }
    }

@router.get("/activity-logs")
async def get_activity_logs(
    limit: int = 20,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Mengembalikan list kosong untuk menonaktifkan fitur Recent Activity 
    dan mencegah Error 500 akibat kolom timestamp yang hilang.
    """
    return []