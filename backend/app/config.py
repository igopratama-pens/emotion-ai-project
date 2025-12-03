"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Emotion AI System"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # API Keys
    GEMINI_API_KEY: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - will be parsed from comma-separated string in .env
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Model
    MODEL_PATH: str = "app/ml/emotion_cnn_fixed.h5"
    IMG_SIZE: int = 100
    MAX_IMAGE_SIZE_MB: int = 5
    
    # Emotions
    EMOTIONS: dict = {
        0: 'Surprise',
        1: 'Fear',
        2: 'Disgust',
        3: 'Happiness',
        4: 'Sadness',
        5: 'Anger',
        6: 'Neutral'
    }
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()