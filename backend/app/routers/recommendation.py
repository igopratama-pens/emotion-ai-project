"""
Recommendation Router (Updated)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendationClickRequest,
    RecommendationClickResponse
)
from ..services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(data: RecommendationRequest):
    """
    Get recommendations based on emotion.
    If category is provided, return only that category.
    If not, return ALL categories (music, food, activity).
    """
    
    # Siapkan wadah hasil
    response_data = {
        "emotion": data.emotion,
        "music": [],
        "food": [],
        "activity": []
    }

    # Logika Cerdas: Ambil paket lengkap jika kategori kosong
    if not data.category or data.category.lower() == 'all':
        # Ambil Music
        music_res = RecommendationService.get_recommendations(data.emotion, 'music')
        if isinstance(music_res, dict) and 'items' in music_res:
            response_data['music'] = music_res['items']
            
        # Ambil Food
        food_res = RecommendationService.get_recommendations(data.emotion, 'food')
        if isinstance(food_res, dict) and 'items' in food_res:
            response_data['food'] = food_res['items']

        # Ambil Activity
        act_res = RecommendationService.get_recommendations(data.emotion, 'activity')
        if isinstance(act_res, dict) and 'items' in act_res:
            response_data['activity'] = act_res['items']

    else:
        # Jika user minta spesifik (jarang dipakai di UI kamu, tapi buat jaga-jaga)
        result = RecommendationService.get_recommendations(data.emotion, data.category)
        # Masukkan ke slot yang sesuai
        if data.category in response_data:
            response_data[data.category] = result.get('items', [])

    return response_data

@router.post("/track", response_model=RecommendationClickResponse)
async def track_recommendation_click(
    data: RecommendationClickRequest,
    db: Session = Depends(get_db)
):
    """Track when user clicks a recommendation"""
    
    result = RecommendationService.track_click(
        emotion=data.emotion,
        category=data.category,
        title=data.title,
        session_id=data.session_id,
        emotion_log_id=data.emotion_log_id,
        db=db
    )
    
    return result

@router.get("/popular")
async def get_popular_recommendations(
    emotion: str = None,
    category: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get most popular recommendations"""
    
    results = RecommendationService.get_popular_recommendations(
        db=db,
        emotion=emotion,
        category=category,
        limit=limit
    )
    
    return {"popular": results}