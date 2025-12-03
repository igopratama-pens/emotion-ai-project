"""
Helper Functions
"""
import random
from typing import Dict, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from ..config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def decode_access_token(token: str) -> Dict:
    """Decode JWT access token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_random_initial_message(emotion: str, confidence: float, face_detected: bool) -> str:
    """
    Generate random initial message based on emotion
    
    Args:
        emotion: Detected emotion
        confidence: Confidence score
        face_detected: Whether face was detected
    
    Returns:
        Initial AI message
    """
    
    messages = {
        'Happiness': [
            "Wow, kamu terlihat bahagia! ✨ Ada kabar baik? Cerita dong!",
            "Senang lihat senyumanmu! 😊 Apa yang bikin harimu spesial?",
            "Kamu kelihatan ceria banget! 🌟 Mau berbagi kebahagiaan ini?"
        ],
        'Sadness': [
            "Aku lihat kamu terlihat sedih 😔 Mau cerita? Aku siap dengar...",
            "Ada yang mengganggu pikiranmu ya? Mau curhat? 💙",
            "Gak apa-apa kok merasa sedih. Yuk, kita bicarain 🤗"
        ],
        'Anger': [
            "Kayaknya ada yang bikin kesal ya 😤 Mau cerita apa yang terjadi?",
            "Sepertinya kamu lagi marah. Yuk kita obrolin pelan-pelan 💪",
            "Aku di sini buat dengerin. Apa yang bikin frustrasi? 🌈"
        ],
        'Fear': [
            "Kamu kelihatan khawatir 😰 Ada yang bikin takut? Cerita aja...",
            "Ada yang bikin cemas? Mau share kekhawatiranmu? 💫",
            "Gak apa-apa merasa takut. Apa yang bisa aku bantu? 🌸"
        ],
        'Surprise': [
            "Wow! Ada yang mengejutkan ya! 😲 Apa yang terjadi?",
            "Kamu kelihatan kaget! Ada kejadian tak terduga? Ceritain! ✨",
            "Wah ada hal menarik ya? Aku penasaran nih! 🎉"
        ],
        'Disgust': [
            "Ada sesuatu yang bikin ga nyaman ya 😖 Mau cerita?",
            "Kayaknya ada yang ganggu pikiran. Apa yang terjadi? 🌿",
            "Ada yang bikin ga enak? Yuk kita obrolin 💚"
        ],
        'Neutral': [
            "Hai! Gimana kabarnya hari ini? 😊",
            "Halo! Ada yang mau diceritain? 💬",
            "Hai! Aku di sini kalau butuh temen ngobrol 🌟"
        ]
    }
    
    msg = random.choice(messages.get(emotion, messages['Neutral']))
    
    if not face_detected:
        msg += "\n\n(Wajah ga kedeteksi, aku analisis dari gambar penuh ya)"
    
    if confidence < 0.5:
        msg += f"\n\n(Confidence {confidence*100:.1f}% - ekspresimu agak samar)"
    
    return msg

def check_crisis_keywords(text: str) -> bool:
    """
    Check if text contains crisis keywords
    
    Args:
        text: Text to check
    
    Returns:
        True if crisis keywords found
    """
    keywords = [
        'bunuh diri', 'ingin mati', 'mengakhiri hidup', 'suicide',
        'potong nadi', 'menyakiti diri', 'self harm', 'tidak ingin hidup',
        'lebih baik mati', 'ingin bunuh diri', 'pengen mati', 'mau mati'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)

def get_emergency_hotlines() -> List[str]:
    """Get emergency mental health hotlines"""
    return [
        "📞 Hotline Kesehatan Mental: 119 ext 8",
        "📞 Into The Light: 021-7851808",
        "📞 Crisis Center Kemenkes: 021-500-454",
        "💬 Sejiwa: 021-5715555 / 0819-1459-6399"
    ]