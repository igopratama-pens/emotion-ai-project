"""
Recommendation Schemas (Updated for Optional Category)
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Any

# Model untuk item rekomendasi tunggal
class RecommendationItem(BaseModel):
    title: str
    description: str
    type: str  # music, food, activity
    link: Optional[str] = None
    image: Optional[str] = None

class RecommendationRequest(BaseModel):
    emotion: str = Field(..., description="Detected emotion")
    # ✅ PERUBAHAN 1: Category sekarang Optional, default None
    category: Optional[str] = Field(None, description="Type: music, food, activity (Optional)")

class RecommendationResponse(BaseModel):
    emotion: str
    # ✅ PERUBAHAN 2: Struktur response disesuaikan dengan Frontend (Detect.tsx)
    # Kita pisahkan list agar frontend mudah menampilkannya
    music: List[RecommendationItem] = []
    food: List[RecommendationItem] = []
    activity: List[RecommendationItem] = []

class RecommendationClickRequest(BaseModel):
    emotion: str
    category: str
    title: str
    session_id: str
    # ✅ PERUBAHAN 3: emotion_log_id jadi Optional (jaga-jaga jika frontend null)
    emotion_log_id: Optional[str] = None

class RecommendationClickResponse(BaseModel):
    status: str