"""
Emotion Recognition System with AI Chat
Complete & Tested Version
"""

import os
import io
import base64
import random
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import numpy as np
import cv2

# TensorFlow
import tensorflow as tf
from tensorflow import keras

# MediaPipe
import mediapipe as mp

# Gemini AI
import google.generativeai as genai

# ============================================================================
# CONFIG
# ============================================================================

GEMINI_API_KEY = "AIzaSyC_1tvKTu022zRaxDb7z_7lgNO32qVURCA"
MODEL_PATH = "model/emotion_cnn.h5"
IMG_SIZE = 100

EMOTIONS = {
    0: 'Surprise',
    1: 'Fear',
    2: 'Disgust',
    3: 'Happiness',
    4: 'Sadness',
    5: 'Anger',
    6: 'Neutral'
}

# ============================================================================
# FASTAPI
# ============================================================================

app = FastAPI(title="Emotion AI Chat", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global
MODEL = None
FACE_DETECTION = None
GEMINI = None

# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup():
    global MODEL, FACE_DETECTION, GEMINI
    
    print("\n" + "="*60)
    print("🚀 STARTING EMOTION AI SYSTEM")
    print("="*60)
    
    # Load CNN
    if os.path.exists(MODEL_PATH):
        print(f"📦 Loading model: {MODEL_PATH}")
        try:
            MODEL = keras.models.load_model(MODEL_PATH)
            print(f"✓ Model loaded: {MODEL.input_shape} → {MODEL.output_shape}")
        except Exception as e:
            print(f"✗ Model error: {e}")
    
    # MediaPipe
    print("📸 Loading MediaPipe...")
    try:
        mp_face = mp.solutions.face_detection
        FACE_DETECTION = mp_face.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )
        print("✓ MediaPipe ready")
    except Exception as e:
        print(f"✗ MediaPipe error: {e}")
    
    # Gemini
    print("🤖 Loading Gemini AI...")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI = genai.GenerativeModel('gemini-2.0-flash')
        print("✓ Gemini ready")
    except Exception as e:
        print(f"✗ Gemini error: {e}")
    
    print("\n✅ Server ready at http://localhost:8000\n")

# ============================================================================
# MODELS
# ============================================================================

class ImageRequest(BaseModel):
    image: str

class ChatRequest(BaseModel):
    emotion: str
    message: str
    history: List[Dict] = []

class PredictionResponse(BaseModel):
    emotion: str
    confidence: float
    initial_message: str
    all_probabilities: Dict[str, float]
    face_detected: bool

class ChatResponse(BaseModel):
    response: str
    emergency: bool = False
    hotlines: Optional[List[str]] = None

# ============================================================================
# IMAGE PROCESSING
# ============================================================================

def detect_face(img: np.ndarray):
    """Detect and crop face"""
    if FACE_DETECTION is None:
        return center_crop(img), False
    
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = FACE_DETECTION.process(rgb)
        
        if results.detections:
            det = results.detections[0]
            box = det.location_data.relative_bounding_box
            
            h, w = img.shape[:2]
            x = int(box.xmin * w)
            y = int(box.ymin * h)
            fw = int(box.width * w)
            fh = int(box.height * h)
            
            # Add margin
            margin = int(0.2 * min(fw, fh))
            x = max(0, x - margin)
            y = max(0, y - margin)
            fw = min(w - x, fw + 2 * margin)
            fh = min(h - y, fh + 2 * margin)
            
            face = img[y:y+fh, x:x+fw]
            if face.size > 0:
                return face, True
        
        return center_crop(img), False
    except:
        return center_crop(img), False

def center_crop(img: np.ndarray):
    """Center crop to square"""
    h, w = img.shape[:2]
    size = min(h, w)
    x = (w - size) // 2
    y = (h - size) // 2
    return img[y:y+size, x:x+size]

def process_image(b64: str):
    """Process base64 to tensor"""
    try:
        # Decode base64
        if ',' in b64:
            b64 = b64.split(',')[1]
        
        img_bytes = base64.b64decode(b64)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img_array = np.array(img)
        
        # BGR for OpenCV
        bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Detect face
        face, detected = detect_face(bgr)
        
        # Back to RGB
        rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        
        # Resize
        resized = cv2.resize(rgb, (IMG_SIZE, IMG_SIZE))
        
        # Normalize
        normalized = resized.astype('float32') / 255.0
        
        # Batch
        batch = np.expand_dims(normalized, axis=0)
        
        return batch, detected
        
    except Exception as e:
        raise HTTPException(400, f"Image error: {e}")

# ============================================================================
# PREDICTION
# ============================================================================

def predict(img_array):
    """Predict emotion"""
    preds = MODEL.predict(img_array, verbose=0)
    probs = preds[0]
    idx = np.argmax(probs)
    conf = float(probs[idx])
    emotion = EMOTIONS[idx]
    return emotion, conf, probs

# ============================================================================
# INITIAL MESSAGES
# ============================================================================

def get_initial_message(emotion: str, conf: float, face: bool):
    """Get initial AI message"""
    
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
    
    if not face:
        msg += "\n\n(Wajah ga kedeteksi, aku analisis dari gambar penuh ya)"
    
    if conf < 0.5:
        msg += f"\n\n(Confidence {conf*100:.1f}% - ekspresimu agak samar)"
    
    return msg

# ============================================================================
# GEMINI CHAT
# ============================================================================

def create_prompt(emotion: str):
    """Create system prompt"""
    
    base = f"""Kamu adalah AI companion yang empatik dan penuh perhatian.
User saat ini merasakan emosi: {emotion}

PERAN:
- Pendengar yang baik dan empati
- Berikan dukungan emosional tulus
- Ajukan pertanyaan terbuka
- Berikan perspektif positif tanpa abaikan perasaan
- Bahasa Indonesia natural dan hangat

GAYA:
- Informal, ramah, hangat
- Emoji secukupnya
- Jangan formal/kaku
- Jawaban singkat 2-4 kalimat
- Fokus mendengar, bukan menggurui

BATASAN:
- BUKAN pengganti profesional kesehatan mental
- Jika ada tanda krisis (bunuh diri, sakiti diri), SEGERA sarankan bantuan profesional
- Jangan diagnosis medis
- Jangan saran medis/terapi spesifik

"""
    
    emotion_guide = {
        'Happiness': "User bahagia! Rayakan, tunjukkan antusiasme.",
        'Sadness': "User sedih. Empati mendalam, validasi perasaan.",
        'Anger': "User marah. Dengar sabar, validasi, jangan perburuk.",
        'Fear': "User takut/cemas. Beri rasa aman, validasi.",
        'Surprise': "User terkejut. Tunjukkan ketertarikan genuine.",
        'Disgust': "User jijik/ga nyaman. Validasi perasaan.",
        'Neutral': "User netral. Ciptakan percakapan hangat."
    }
    
    return base + emotion_guide.get(emotion, emotion_guide['Neutral'])

def check_crisis(text: str):
    """Check crisis keywords"""
    keywords = [
        'bunuh diri', 'ingin mati', 'mengakhiri hidup', 'suicide',
        'potong nadi', 'menyakiti diri', 'self harm', 'tidak ingin hidup',
        'lebih baik mati', 'ingin bunuh diri', 'pengen mati'
    ]
    lower = text.lower()
    return any(k in lower for k in keywords)

async def chat_gemini(emotion: str, user_msg: str, history: List[Dict]):
    """Chat with Gemini"""
    
    if GEMINI is None:
        raise HTTPException(503, "Gemini not available")
    
    try:
        # Check crisis
        is_crisis = check_crisis(user_msg)
        
        # Build prompt
        prompt = create_prompt(emotion)
        prompt += "\n\nPERCAKAPAN:\n"
        
        # Add history (last 5)
        for msg in history[-5:]:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt += f"{role.upper()}: {content}\n"
        
        prompt += f"USER: {user_msg}\nASSISTANT:"
        
        # Generate
        response = GEMINI.generate_content(prompt)
        ai_msg = response.text.strip()
        
        # Crisis handling
        hotlines = None
        if is_crisis:
            ai_msg += "\n\n⚠️ Aku sangat peduli denganmu. Tolong hubungi bantuan profesional:"
            hotlines = [
                "📞 Hotline Kesehatan Mental: 119 ext 8",
                "📞 Into The Light: 021-7851808",
                "📞 Crisis Center Kemenkes: 021-500-454",
                "💬 Sejiwa: 021-5715555 / 0819-1459-6399"
            ]
        
        return {
            "response": ai_msg,
            "emergency": is_crisis,
            "hotlines": hotlines
        }
        
    except Exception as e:
        print(f"Gemini error: {e}")
        raise HTTPException(500, f"Chat error: {e}")

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve HTML"""
    html_path = "templates/index.html"
    
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    
    return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Emotion AI</title></head>
        <body style="font-family:Arial;max-width:800px;margin:50px auto;padding:20px;">
            <h1>🎭 Emotion AI System</h1>
            <p>✅ Server is running</p>
            <p>⚠️ Place HTML at: <code>templates/index.html</code></p>
            <p>📖 <a href="/docs">API Docs</a></p>
        </body>
        </html>
    """)

@app.post("/predict", response_model=PredictionResponse)
async def predict_emotion(req: ImageRequest):
    """Predict emotion"""
    
    if MODEL is None:
        raise HTTPException(503, "Model not loaded")
    
    try:
        # Process image
        img_array, face_detected = process_image(req.image)
        
        # Predict
        emotion, conf, probs = predict(img_array)
        
        # Initial message
        init_msg = get_initial_message(emotion, conf, face_detected)
        
        # Format probs
        prob_dict = {EMOTIONS[i]: float(probs[i]) for i in range(len(EMOTIONS))}
        
        return PredictionResponse(
            emotion=emotion,
            confidence=conf,
            initial_message=init_msg,
            all_probabilities=prob_dict,
            face_detected=face_detected
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Prediction error: {e}")

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Chat with AI"""
    
    try:
        result = await chat_gemini(req.emotion, req.message, req.history)
        return ChatResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Chat error: {e}")

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "ok",
        "model": MODEL is not None,
        "face_detection": FACE_DETECTION is not None,
        "gemini": GEMINI is not None,
        "emotions": list(EMOTIONS.values())
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🎭 EMOTION AI SYSTEM")
    print("="*60)
    print("Starting server...")
    print("Open: http://localhost:8000")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")