"""
Chat Service with Gemini AI
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import google.generativeai as genai
from ..models.chat_log import ChatLog
from ..config import settings
from ..utils.helpers import check_crisis_keywords, get_emergency_hotlines

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
# ✅ FIX: Menggunakan model yang lebih stabil/terbaru
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

class ChatService:
    """Service for AI chat"""
    
    @staticmethod
    def create_system_prompt(emotion: str) -> str:
        """Create system prompt based on emotion"""
        
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
- Emoji secukupnya (1-2 per pesan)
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
            'Happiness': "User bahagia! Rayakan, tunjukkan antusiasme, dorong berbagi lebih.",
            'Sadness': "User sedih. Empati mendalam, validasi perasaan, beri ruang cerita.",
            'Anger': "User marah. Dengar sabar, validasi kemarahan, jangan perburuk.",
            'Fear': "User takut/cemas. Beri rasa aman, validasi kekhawatiran.",
            'Surprise': "User terkejut. Tunjukkan ketertarikan genuine, bantu proses.",
            'Disgust': "User jijik/ga nyaman. Validasi perasaan, bantu bicara.",
            'Neutral': "User netral. Ciptakan percakapan hangat, undang berbagi."
        }
        
        return base + emotion_guide.get(emotion, emotion_guide['Neutral'])
    
    @staticmethod
    async def chat(
        emotion: str,
        user_message: str,
        session_id: str,
        emotion_log_id: str,
        chat_history: List[Dict],
        db: Session
    ) -> Dict:
        """
        Chat with Gemini AI
        """
        
        # Check for crisis
        is_crisis = check_crisis_keywords(user_message)
        
        # Build prompt
        prompt = ChatService.create_system_prompt(emotion)
        prompt += "\n\nPERCAKAPAN:\n"
        
        # Add history (last 5 messages for context)
        for msg in chat_history[-5:]:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt += f"{role.upper()}: {content}\n"
        
        prompt += f"USER: {user_message}\nASSISTANT:"
        
        try:
            # ✅ FIX: Generate response with explicit config
            response = gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=512,
                )
            )
            ai_response = response.text.strip()
            
            # Add crisis resources if needed
            hotlines = None
            if is_crisis:
                ai_response += "\n\n⚠️ Aku sangat peduli denganmu. Tolong hubungi bantuan profesional:"
                hotlines = get_emergency_hotlines()
            
            # Save user message to DB
            user_log = ChatLog(
                # ✅ FIX: Handle empty string for UUID conversion later
                emotion_log_id=emotion_log_id if emotion_log_id else None,
                session_id=session_id,
                message=user_message,
                response="",  # User message doesn't have response
                is_user=True,
                is_crisis=is_crisis
            )
            db.add(user_log)
            
            # Save AI response to DB
            ai_log = ChatLog(
                # ✅ FIX: Handle empty string for UUID conversion later
                emotion_log_id=emotion_log_id if emotion_log_id else None,
                session_id=session_id,
                message="",  # AI response doesn't have user message
                response=ai_response,
                is_user=False,
                is_crisis=is_crisis
            )
            db.add(ai_log)
            
            db.commit()
            
            return {
                "response": ai_response,
                "emergency": is_crisis,
                "hotlines": hotlines
            }
            
        except Exception as e:
            print(f"Gemini error: {e}")
            db.rollback() # ✅ FIX: Rollback transaction on error
            
            # ✅ FIX: Fallback responses based on emotion
            fallback_responses = {
                'Happiness': "Senang melihatmu bahagia! Cerita lebih banyak dong tentang apa yang membuatmu senang? 😊",
                'Sadness': "Aku di sini untukmu. Mau cerita apa yang membuatmu sedih? 💙",
                'Anger': "Aku dengar kamu. Apa yang membuatmu marah? Mari kita bicara. 💪",
                'Fear': "Tidak apa-apa merasa takut. Aku di sini. Mau cerita lebih lanjut? 🌸",
                'Surprise': "Wah! Ada apa? Ceritakan! ✨",
                'Disgust': "Sepertinya ada yang mengganggu. Mau cerita? 🌿",
                'Neutral': "Hai! Bagaimana harimu? Ada yang mau diceritakan? 💬"
            }
            
            fallback_message = fallback_responses.get(
                emotion, 
                "Maaf, aku sedang mengalami gangguan. Tapi aku tetap di sini untukmu. Coba lagi ya 🙏"
            )
            
            return {
                "response": fallback_message,
                "emergency": is_crisis,
                "hotlines": get_emergency_hotlines() if is_crisis else None
            }
    
    @staticmethod
    def get_chat_history(
        db: Session,
        session_id: str = None,
        emotion_log_id: str = None,
        limit: int = 50
    ):
        """Get chat history"""
        query = db.query(ChatLog)
        
        if session_id:
            query = query.filter(ChatLog.session_id == session_id)
        
        if emotion_log_id:
            query = query.filter(ChatLog.emotion_log_id == emotion_log_id)
        
        return query.order_by(ChatLog.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def get_crisis_chats(db: Session, limit: int = 100):
        """Get chats with crisis detection"""
        return db.query(ChatLog).filter(
            ChatLog.is_crisis == True
        ).order_by(ChatLog.timestamp.desc()).limit(limit).all()