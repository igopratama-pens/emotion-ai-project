# 🎭 Emotion AI System

**AI-Powered Mental Health Companion untuk Remaja dan Mahasiswa**

## 👥 Anggota Kelompok (Our Team)

| Nama | NIM | Peran |
| :--- | :--- | :--- |
| **Muhammad Igo Pratama** | 3323600031 | Data Scientist / Model Training |
| **Alrahma Dinda Salsabila** | 3323600038 | Backend Developer |
| **Evinda Eka Ayudia Lestari** | 3323600039 | Backend Developer |
| **Nur Aghni Rizqiyah Baharawi** | 3323600058 | Frontend Developer |
| **R.Aj Maria Shovia Fadinda** | 3323600059 | Frontend Developer |

> Sistem deteksi emosi real-time dengan AI chatbot empathic dan rekomendasi personal menggunakan Deep Learning, FastAPI, dan React.

---

## 📋 Daftar Isi

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Performance](#-model-performance)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Team](#-team)

---

## 🎯 Overview

**Emotion AI System** adalah aplikasi web full-stack yang menggunakan Computer Vision dan Natural Language Processing untuk membantu remaja dan mahasiswa memahami dan mengelola emosi mereka. Sistem ini menggabungkan:

- **Real-time Emotion Detection**: Deteksi 7 emosi dasar dari ekspresi wajah
- **Empathic AI Chatbot**: Conversational AI yang responsif terhadap emosi user
- **Personalized Recommendations**: Rekomendasi musik, makanan, dan aktivitas berdasarkan mood
- **Crisis Detection**: Deteksi otomatis kata kunci berbahaya dan emergency resources

### Target User
- 🎓 **Mahasiswa**: Self-awareness dan stress management
- 👥 **Remaja**: Emotional literacy dan mental wellness

### Problem Statement
Di era digital, banyak remaja dan mahasiswa mengalami kesulitan memahami dan mengekspresikan emosi mereka. Kurangnya akses ke mental health resources dan stigma sosial membuat mereka enggan mencari bantuan profesional.

### Solution
Platform digital yang:
1. Membantu user mengenali emosi mereka secara objektif
2. Menyediakan AI companion yang empatik dan non-judgmental
3. Memberikan coping strategies melalui rekomendasi personal
4. Mendeteksi kondisi kritis dan menyediakan emergency contacts

---

## ✨ Features

### 🔍 Core Features

#### 1. Real-time Emotion Detection
- **Webcam Integration**: Capture foto wajah langsung dari browser
- **Face Detection**: Deteksi wajah otomatis menggunakan MediaPipe
- **7 Emotion Classification**: 
  - 😊 Happiness (Bahagia)
  - 😔 Sadness (Sedih)
  - 😤 Anger (Marah)
  - 😰 Fear (Takut)
  - 😲 Surprise (Terkejut)
  - 😒 Disgust (Jijik)
  - 😐 Neutral (Netral)
- **Confidence Score**: Tingkat kepercayaan prediksi (%)
- **Probability Distribution**: Visualisasi probabilitas semua emosi

#### 2. Empathic AI Chatbot
- **Context-Aware**: Merespon sesuai emosi yang terdeteksi
- **Natural Conversation**: Bahasa Indonesia yang natural dan hangat
- **Crisis Detection**: Deteksi kata kunci berbahaya (bunuh diri, self-harm)
- **Emergency Resources**: Auto-suggest hotlines saat terdeteksi krisis
- **Powered by**: Google Gemini 2.0 Flash

#### 3. Personalized Recommendations
Berdasarkan emosi terdeteksi, user mendapat rekomendasi:
- 🎵 **Music**: Playlist YouTube yang sesuai mood
- 🍽️ **Food**: Makanan comfort atau energizing
- 🎯 **Activity**: Kegiatan coping yang sehat

#### 4. Admin Dashboard
- 📊 **Analytics**: Total users, emosi terbanyak, trends
- 📈 **Charts**: Visualisasi distribusi emosi
- 🔝 **Popular Recommendations**: Tracking rekomendasi terpopuler
- 📝 **User Logs**: Riwayat deteksi dan chat
- 🚨 **Crisis Alerts**: Monitor chat dengan flag krisis

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL + SQLAlchemy ORM
- **AI/ML**: 
  - TensorFlow 2.15.0 (CNN Model)
  - Google Generative AI (Gemini)
  - MediaPipe 0.10.8 (Face Detection)
  - OpenCV 4.8.1 (Image Processing)
- **Authentication**: JWT (python-jose)
- **Migration**: Alembic

### Frontend
- **Framework**: React 18.3.1 + TypeScript
- **Build Tool**: Vite 5.4
- **UI Components**: shadcn/ui + Radix UI
- **Styling**: TailwindCSS 3.4
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Routing**: React Router DOM 6.30
- **Webcam**: react-webcam 7.2

### Machine Learning
- **Model**: Custom CNN
- **Architecture**: 3 Convolutional Blocks + BatchNormalization + Dropout
- **Input**: 100x100x3 RGB images
- **Output**: 7-class softmax probabilities
- **Dataset**: RAF-DB (Real-world Affective Faces Database)
- **Performance**: 76.3% accuracy on test set

### DevOps
- **Server**: Uvicorn (ASGI)
- **CORS**: Enabled for frontend-backend communication
- **Logging**: TensorBoard + Custom logs

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │   Webcam     │────────▶│  React App   │                 │
│  │  Capture     │         │  (Frontend)  │                 │
│  └──────────────┘         └───────┬──────┘                 │
└──────────────────────────────────┼────────────────────────┘
                                    │ HTTP/REST API
                                    │
┌───────────────────────────────────▼────────────────────────┐
│                      FASTAPI BACKEND                        │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │   Emotion    │  │     Chat     │  │ Recommendation  │ │
│  │   Router     │  │    Router    │  │     Router      │ │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘ │
│         │                 │                    │          │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌────────▼────────┐ │
│  │   Emotion    │  │     Chat     │  │ Recommendation  │ │
│  │   Service    │  │   Service    │  │    Service      │ │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘ │
│         │                 │                    │          │
│  ┌──────▼───────┐  ┌──────▼────────────────────▼────────┐ │
│  │  MediaPipe   │  │      PostgreSQL Database           │ │
│  │Face Detection│  │  (EmotionLog, ChatLog, ClickLog)   │ │
│  └──────┬───────┘  └────────────────────────────────────┘ │
│         │                                                  │
│  ┌──────▼───────┐  ┌──────────────┐                      │
│  │  CNN Model   │  │    Gemini    │                      │
│  │(emotion_cnn) │  │   AI Chat    │                      │
│  └──────────────┘  └──────────────┘                      │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

**1. Emotion Detection Flow**
```
User clicks "Capture" 
→ Webcam captures image (Base64)
→ POST /api/emotion/detect
→ MediaPipe detects face
→ Crop & resize to 100x100
→ CNN predicts emotion
→ Save to EmotionLog
→ Return emotion + confidence + recommendations
```

**2. Chat Flow**
```
User types message
→ POST /api/chat/send
→ Load emotion context
→ Check crisis keywords
→ Generate Gemini prompt with emotion context
→ Get AI response
→ Save to ChatLog
→ Return response (+ emergency hotlines if crisis)
```

**3. Recommendation Flow**
```
User requests recommendations
→ GET /api/recommendations?emotion=X&category=Y
→ Fetch from recommendation database
→ User clicks recommendation
→ POST /api/recommendations/track
→ Save to RecommendationClick (for analytics)
```

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Git

### 1. Clone Repository
```bash
git clone <repository-url>
cd emotion-ai-system
```

### 2. Backend Setup

#### a. Create Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### b. Install Dependencies
```bash
pip install -r requirements.txt
```

#### c. Environment Variables
Create `.env` file in `backend/` folder:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emotion_ai_db

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Security
SECRET_KEY=your_secret_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_admin_password

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# App
APP_NAME=Emotion AI System
DEBUG=True
```

#### d. Database Migration
```bash
# Create database first in PostgreSQL
createdb emotion_ai_db

# Run migrations
alembic upgrade head
```

#### e. Add ML Model
Place `emotion_cnn.h5` model file in:
```
backend/app/ml/emotion_cnn.h5
```

#### f. Run Backend
```bash
# Development
uvicorn app.main:app --reload --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend will run at: `http://localhost:8000`  
API Docs: `http://localhost:8000/api/docs`

### 3. Frontend Setup

#### a. Install Dependencies
```bash
cd frontend
npm install
```

#### b. Environment Variables
Create `.env.local` file in `frontend/` folder:
```env
VITE_API_URL=http://localhost:8000
```

#### c. Run Frontend
```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

Frontend will run at: `http://localhost:5173`

---

## 🚀 Usage

### For Users

#### 1. Access Application
Open browser and navigate to `http://localhost:5173`

#### 2. Emotion Detection
1. Click **"Start Camera"** → Allow camera permission
2. Position your face in frame
3. Click **"Capture Photo"**
4. Wait for emotion analysis (~2 seconds)
5. View detected emotion + confidence score

#### 3. Get Recommendations
1. After emotion detected, choose category:
   - 🎵 Music
   - 🍽️ Food
   - 🎯 Activity
2. Browse recommendations
3. Click links to access content

#### 4. Chat with AI
1. Click **"Chat"** button
2. Share your feelings
3. AI responds empathetically based on your emotion
4. If crisis detected, emergency resources shown

### For Admin

#### 1. Login
Navigate to `/admin-login` and use credentials from `.env`

#### 2. Dashboard Features
- **Overview Stats**: Total users, detections, chats
- **Emotion Distribution**: Pie/bar chart of emotions
- **Popular Recommendations**: Most clicked items
- **Recent Activity**: Latest user interactions
- **User Logs**: View detailed history
- **Crisis Monitoring**: Flagged conversations

---

## 📊 Model Performance

### CNN Architecture

```python
Input (100x100x3)
    ↓
Conv2D(64, 3x3) + BatchNorm + ReLU + MaxPool + Dropout(0.25)
    ↓
Conv2D(64, 3x3) + BatchNorm + ReLU + MaxPool + Dropout(0.25)
    ↓
Conv2D(32, 3x3) + BatchNorm + ReLU + MaxPool + Dropout(0.25)
    ↓
Flatten
    ↓
Dense(128) + BatchNorm + Dropout(0.5)
    ↓
Dense(7, softmax)
```

**Parameters**: ~150,000  
**Model Size**: ~3 MB  
**Inference Time**: 20-50ms

### Dataset

- **Source**: RAF-DB (Real-world Affective Faces Database)
- **Train Set**: 12,271 images
- **Test Set**: 3,068 images
- **Classes**: 7 emotions (balanced via class weighting)
- **Augmentation**: Rotation, flip, zoom, shift

### Performance Metrics

**Overall Accuracy**: 76.30%

| Emotion    | Precision | Recall | F1-Score | Support |
|------------|-----------|--------|----------|---------|
| Surprise   | 82.65%    | 73.86% | 78.01%   | 329     |
| Fear       | 76.32%    | 39.19% | 51.79%   | 74      |
| Disgust    | 53.45%    | 19.38% | 28.44%   | 160     |
| Happiness  | 88.34%    | 88.86% | 88.60%   | 1185    |
| Sadness    | 68.31%    | 66.74% | 67.51%   | 478     |
| Anger      | 59.89%    | 67.28% | 63.37%   | 162     |
| Neutral    | 66.55%    | 81.91% | 73.43%   | 680     |

### Analysis

**Best Performance**:
- ✅ Happiness (88.6% F1) - Most data, clear features
- ✅ Neutral (73.4% F1) - Common baseline emotion

**Challenges**:
- ⚠️ Disgust (28.4% F1) - Limited data, subtle expressions
- ⚠️ Fear (51.8% F1) - Often confused with Surprise
- ⚠️ Anger (63.4% F1) - Similar to Disgust features

**Common Confusions**:
1. Fear ↔ Surprise (wide eyes, open mouth)
2. Anger ↔ Disgust (furrowed brows)
3. Sadness ↔ Neutral (subtle differences)

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Emotion Detection

**POST** `/api/emotion/detect`

Detect emotion from image.

**Request Body**:
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "session_id": "uuid-v4-string"
}
```

**Response**:
```json
{
  "emotion": "Happiness",
  "confidence": 87.3,
  "probabilities": {
    "Happiness": 87.3,
    "Neutral": 8.2,
    "Surprise": 2.1,
    "Sadness": 1.5,
    "Anger": 0.5,
    "Fear": 0.3,
    "Disgust": 0.1
  },
  "message": "Senang melihat kamu bahagia! 😊",
  "emotion_log_id": "uuid",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Chat with AI

**POST** `/api/chat/send`

Send message to AI chatbot.

**Request Body**:
```json
{
  "message": "Aku lagi stress banget nih",
  "session_id": "uuid-v4-string",
  "emotion_log_id": "uuid",
  "emotion": "Sadness"
}
```

**Response**:
```json
{
  "response": "Aku dengar kamu lagi stress ya. Boleh cerita lebih banyak ga, apa yang bikin kamu stress? 💙",
  "emergency": false,
  "hotlines": null
}
```

**Crisis Response Example**:
```json
{
  "response": "Aku sangat peduli denganmu. Tolong hubungi bantuan profesional:",
  "emergency": true,
  "hotlines": [
    {
      "name": "Sehat Jiwa (Kemenkes RI)",
      "phone": "119 ext 8"
    },
    {
      "name": "Into The Light Indonesia",
      "phone": "021-78842580",
      "hours": "24/7"
    }
  ]
}
```

#### 3. Get Recommendations

**GET** `/api/recommendations?emotion={emotion}&category={category}`

Get personalized recommendations.

**Parameters**:
- `emotion`: Happiness | Sadness | Anger | Fear | Surprise | Disgust | Neutral
- `category`: music | food | activity

**Response**:
```json
{
  "emotion": "Happiness",
  "category": "music",
  "items": [
    {
      "title": "Happy - Pharrell Williams",
      "description": "Musik upbeat untuk memperbesar kebahagiaanmu!",
      "type": "music",
      "link": "https://www.youtube.com/watch?v=...",
      "image": null
    }
  ],
  "description": "Musik upbeat untuk memperbesar kebahagiaanmu! 🎵"
}
```

#### 4. Track Recommendation Click

**POST** `/api/recommendations/track`

Track when user clicks a recommendation.

**Request Body**:
```json
{
  "emotion": "Happiness",
  "category": "music",
  "title": "Happy - Pharrell Williams",
  "session_id": "uuid",
  "emotion_log_id": "uuid"
}
```

#### 5. Admin - Get Stats

**GET** `/api/admin/stats?days=7`

Get dashboard statistics (requires authentication).

**Response**:
```json
{
  "total_users": 523,
  "total_detections": 1247,
  "total_chats": 892,
  "emotion_distribution": {
    "Happiness": 35.2,
    "Neutral": 28.1,
    "Sadness": 15.3,
    "Surprise": 8.7,
    "Anger": 6.2,
    "Fear": 4.5,
    "Disgust": 2.0
  },
  "popular_recommendations": [...]
}
```

---

## 📁 Project Structure

```
emotion-ai-system/
│
├── backend/                        # FastAPI Backend
│   ├── app/
│   │   ├── routers/               # API endpoints
│   │   │   ├── emotion.py         # Emotion detection routes
│   │   │   ├── chat.py            # Chat routes
│   │   │   ├── recommendation.py  # Recommendation routes
│   │   │   └── admin.py           # Admin routes
│   │   ├── services/              # Business logic
│   │   │   ├── emotion_service.py
│   │   │   ├── chat_service.py
│   │   │   └── recommendation_service.py
│   │   ├── models/                # SQLAlchemy models
│   │   │   ├── emotion_log.py
│   │   │   ├── chat_log.py
│   │   │   └── recommendation_click.py
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── ml/                    # ML models
│   │   │   ├── model_loader.py
│   │   │   └── emotion_cnn.h5     # Trained CNN model
│   │   ├── utils/                 # Utilities
│   │   │   ├── face_detection.py  # MediaPipe integration
│   │   │   ├── image_processing.py
│   │   │   └── helpers.py         # Crisis detection, etc.
│   │   ├── main.py                # FastAPI app
│   │   ├── config.py              # Configuration
│   │   └── database.py            # Database connection
│   ├── alembic/                   # Database migrations
│   ├── requirements.txt
│   └── .env
│
├── frontend/                       # React Frontend
│   ├── src/
│   │   ├── pages/                 # Page components
│   │   │   ├── Home.tsx
│   │   │   ├── Detect.tsx         # Main emotion detection page
│   │   │   ├── Dashboard.tsx      # Admin dashboard
│   │   │   └── AdminLogin.tsx
│   │   ├── components/            # Reusable components
│   │   │   ├── ui/                # shadcn/ui components
│   │   │   ├── Navbar.tsx
│   │   │   └── ChatBubble.tsx
│   │   ├── services/              # API clients
│   │   │   ├── emotionApi.ts
│   │   │   ├── chatApi.ts
│   │   │   └── recommendationApi.ts
│   │   ├── context/               # React Context
│   │   │   ├── EmotionContext.tsx
│   │   │   ├── ChatContext.tsx
│   │   │   └── AuthContext.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── .env.local
│
├── app_lama/                       # Legacy monolithic version
│   ├── model/
│   │   └── emotion_cnn.h5         # Source model
│   ├── results/                   # Training visualizations
│   └── train_model.py             # Training script
│
├── data/                          # Dataset (RAF-DB)
│   └── DATASET/
│       ├── train/
│       └── test/
│
└── README.md                      # This file
```

---

## 👥 Team

**[Nama Kelompok]**

- **[Nama Anggota 1]** - [NPM] - [Role]
- **[Nama Anggota 2]** - [NPM] - [Role]
- **[Nama Anggota 3]** - [NPM] - [Role]

**Dosen Pembimbing**: [Nama Dosen]

**Program Studi**: [Nama Prodi]  
**Universitas**: [Nama Universitas]  
**Tahun**: 2024

---

## 📚 References

1. **RAF-DB Dataset**:
   - Li, S., Deng, W., & Du, J. (2017). "Reliable Crowdsourcing and Deep Locality-Preserving Learning for Expression Recognition in the Wild", CVPR 2017.

2. **MediaPipe**:
   - Google Research. MediaPipe Face Detection.
   - https://google.github.io/mediapipe/

3. **CNN Architectures**:
   - LeCun, Y., et al. "Gradient-Based Learning Applied to Document Recognition", IEEE 1998.

4. **Mental Health Resources**:
   - WHO. "Mental Health Action Plan 2013-2030"
   - Kemenkes RI. "Pedoman Kesehatan Jiwa Remaja"

---

## 📄 License

This project is created for educational purposes (Final Project / Proyek Akhir).

---

## 🙏 Acknowledgments

- Dataset: RAF-DB (Li et al., 2017)
- AI: Google Gemini 2.0 Flash
- Face Detection: Google MediaPipe
- UI Components: shadcn/ui
- Framework: FastAPI, React

---

**Built with ❤️ for Mental Health Awareness**

*Helping students understand and manage their emotions through AI technology*

---

## 🔧 Troubleshooting

### Backend Issues

**1. Model tidak load**
```bash
# Pastikan file model ada
ls backend/app/ml/emotion_cnn.h5

# Check TensorFlow version
pip show tensorflow
```

**2. Database connection error**
```bash
# Check PostgreSQL running
pg_isready

# Verify connection string in .env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

**3. Gemini API error**
```bash
# Verify API key in .env
GEMINI_API_KEY=your_key_here

# Test API key
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print('OK')"
```

### Frontend Issues

**1. CORS error**
- Check `ALLOWED_ORIGINS` in backend `.env`
- Verify `VITE_API_URL` in frontend `.env.local`

**2. Webcam tidak muncul**
- Check browser permissions
- Try different browser (Chrome recommended)
- Use HTTPS in production

**3. Build error**
```bash
# Clear node_modules
rm -rf node_modules package-lock.json
npm install
```