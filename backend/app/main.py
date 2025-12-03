"""
FastAPI Main Application
Emotion AI System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .routers import emotion, chat, recommendation, admin
from .ml.model_loader import emotion_model

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Emotion Recognition System with AI Chat and Recommendations",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(emotion.router)
app.include_router(chat.router)
app.include_router(recommendation.router)
app.include_router(admin.router)

@app.on_event("startup")
async def startup_event():
    """Load ML model on startup"""
    print("\n" + "="*60)
    print("🚀 EMOTION AI SYSTEM - STARTING")
    print("="*60)
    
    # Load emotion detection model
    try:
        emotion_model.load_model()
        print("✓ Emotion detection model loaded")
    except Exception as e:
        print(f"⚠ Warning: Could not load model: {e}")
    
    print(f"\n✅ API ready at http://localhost:8000")
    print(f"📖 Docs at http://localhost:8000/api/docs")
    print("="*60 + "\n")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": emotion_model.is_loaded,
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🎭 EMOTION AI SYSTEM")
    print("="*60)
    print("Starting server...")
    print("API: http://localhost:8000")
    print("Docs: http://localhost:8000/api/docs")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )