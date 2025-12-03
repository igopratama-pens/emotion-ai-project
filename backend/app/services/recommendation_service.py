from sqlalchemy.orm import Session
from typing import Dict, List
from ..models.recommendation_click import RecommendationClick
import uuid

class RecommendationService:
    """Service for recommendations"""
    
    # Recommendation database
    # NOTE: Link makanan diganti ke Google Maps Search agar dinamis sesuai lokasi user
    RECOMMENDATIONS = {
        'Happiness': {
            'music': {
                'items': [
                    {'title': 'Happy - Pharrell Williams', 'link': 'https://www.youtube.com/watch?v=ZbZSe6N_BXs', 'type': 'youtube'},
                    {'title': 'Don\'t Stop Me Now - Queen', 'link': 'https://www.youtube.com/watch?v=HgzGwKwLmgM', 'type': 'youtube'},
                    {'title': 'Walking on Sunshine - Katrina', 'link': 'https://www.youtube.com/watch?v=iPUmE-tne5U', 'type': 'youtube'},
                    {'title': 'Good Vibrations - Beach Boys', 'link': 'https://www.youtube.com/watch?v=Eab_beh07HU', 'type': 'youtube'}
                ],
                'description': 'Musik upbeat untuk memperbesar kebahagiaanmu! 🎵'
            },
            'food': {
                'items': [
                    {'title': 'Pizza Party 🍕', 'link': 'https://www.google.com/maps/search/pizza+near+me', 'description': 'Pizza favorit di sekitarmu'},
                    {'title': 'Sweet Desserts 🍰', 'link': 'https://www.google.com/maps/search/cake+bakery+near+me', 'description': 'Dessert manis untuk merayakan hari'},
                    {'title': 'Fresh Smoothie 🍓', 'link': 'https://www.google.com/maps/search/smoothie+juice+bar+near+me', 'description': 'Minuman segar penuh warna'}
                ],
                'description': 'Makanan ceria untuk suasana hati yang ceria! 🌈'
            },
            'activity': {
                'items': [
                    'Panggil teman untuk hang out atau video call 📞',
                    'Main game favorit atau coba game baru 🎮',
                    'Buat konten kreatif (foto, video, gambar) 🎨',
                    'Olahraga ringan atau dance challenge 💃',
                    'Tulis hal-hal yang bikin kamu grateful hari ini ✍️'
                ],
                'description': 'Aktivitas seru untuk merayakan kebahagiaan! 🎉'
            }
        },
        'Sadness': {
            'music': {
                'items': [
                    {'title': 'Fix You - Coldplay', 'link': 'https://www.youtube.com/watch?v=k4V3Mo61fJM', 'type': 'youtube'},
                    {'title': 'Someone Like You - Adele', 'link': 'https://www.youtube.com/watch?v=hLQl3WQQoQ0', 'type': 'youtube'},
                    {'title': 'The Scientist - Coldplay', 'link': 'https://www.youtube.com/watch?v=RB-RcX5DS5A', 'type': 'youtube'}
                ],
                'description': 'Musik untuk pelepasan emosional yang sehat 💙'
            },
            'food': {
                'items': [
                    {'title': 'Warm Soup 🍜', 'link': 'https://www.google.com/maps/search/warm+soup+near+me', 'description': 'Sup hangat yang menenangkan hati'},
                    {'title': 'Hot Chocolate ☕', 'link': 'https://www.google.com/maps/search/hot+chocolate+cafe+near+me', 'description': 'Coklat panas yang nyaman'},
                    {'title': 'Comfort Food (Pasta/Rice) 🍝', 'link': 'https://www.google.com/maps/search/comfort+food+restaurant+near+me', 'description': 'Makanan yang bikin perut nyaman'}
                ],
                'description': 'Makanan hangat yang bikin nyaman 🤗'
            },
            'activity': {
                'items': [
                    'Journaling - tulis apa yang kamu rasakan ✍️',
                    'Tonton film atau series comfort favoritmu 🎬',
                    'Cuddle dengan pet atau boneka kesayangan 🧸',
                    'Mandi air hangat dengan musik tenang 🛁',
                    'Chat atau telpon orang yang kamu percaya 💬'
                ],
                'description': 'Aktivitas menenangkan untuk dirimu 🌙'
            }
        },
        'Anger': {
            'music': {
                'items': [
                    {'title': 'Lose Yourself - Eminem', 'link': 'https://www.youtube.com/watch?v=_Yhyp-_hX2s', 'type': 'youtube'},
                    {'title': 'Eye of the Tiger - Survivor', 'link': 'https://www.youtube.com/watch?v=btPJPFnesV4', 'type': 'youtube'},
                    {'title': 'Radioactive - Imagine Dragons', 'link': 'https://www.youtube.com/watch?v=ktvTqknDobU', 'type': 'youtube'}
                ],
                'description': 'Musik berenergi untuk release tension 💪'
            },
            'food': {
                'items': [
                    {'title': 'Spicy Wings/Food 🔥', 'link': 'https://www.google.com/maps/search/spicy+food+near+me', 'description': 'Makanan pedas untuk melepaskan emosi'},
                    {'title': 'Juicy Burger 🍔', 'link': 'https://www.google.com/maps/search/burger+near+me', 'description': 'Burger besar yang memuaskan'},
                    {'title': 'Cold Drink/Ice Cream 🍦', 'link': 'https://www.google.com/maps/search/ice+cream+near+me', 'description': 'Dinginkan kepalamu dengan yang dingin'}
                ],
                'description': 'Makanan bold yang match energimu! 🌶️'
            },
            'activity': {
                'items': [
                    'Olahraga intensif (boxing, lari, HIIT) 🥊',
                    'Punch pillow atau stress ball 😤',
                    'Tulis surat kemarahan (ga perlu dikirim) ✍️',
                    'Bersih-bersih ruangan dengan energik 🧹',
                    'Teriak di tempat sepi atau dalam bantal 📢'
                ],
                'description': 'Channel kemarahanmu ke hal produktif! 💥'
            }
        },
        'Fear': {
            'music': {
                'items': [
                    {'title': 'Brave - Sara Bareilles', 'link': 'https://www.youtube.com/watch?v=QUQsqBqxoR4', 'type': 'youtube'},
                    {'title': 'Stronger - Kelly Clarkson', 'link': 'https://www.youtube.com/watch?v=Xn676-fLq7I', 'type': 'youtube'},
                    {'title': 'Hall of Fame - The Script', 'link': 'https://www.youtube.com/watch?v=mk48xRzuNvA', 'type': 'youtube'}
                ],
                'description': 'Musik motivasi untuk boost keberanian! 💫'
            },
            'food': {
                'items': [
                    {'title': 'Herbal Tea (Chamomile) 🍵', 'link': 'https://www.google.com/maps/search/tea+house+near+me', 'description': 'Teh herbal untuk menenangkan saraf'},
                    {'title': 'Warm Milk/Latte 🥛', 'link': 'https://www.google.com/maps/search/warm+milk+coffee+near+me', 'description': 'Minuman hangat yang gentle'},
                    {'title': 'Healthy Smoothie 🍌', 'link': 'https://www.google.com/maps/search/healthy+smoothie+near+me', 'description': 'Nutrisi baik untuk tubuhmu'}
                ],
                'description': 'Makanan menenangkan untuk kurangi kecemasan 🌸'
            },
            'activity': {
                'items': [
                    'Latihan pernapasan 4-7-8 (inhale 4s, hold 7s, exhale 8s) 🧘',
                    'Grounding technique: sebutkan 5 hal yang kamu lihat, 4 yang kamu dengar, dst 👀',
                    'Tonton video lucu atau wholesome 😊',
                    'Chat dengan orang yang bikin kamu merasa aman 💬',
                    'Yoga atau stretching ringan 🧘‍♀️'
                ],
                'description': 'Teknik menenangkan untuk atasi ketakutan 🌈'
            }
        },
        'Surprise': {
            'music': {
                'items': [
                    {'title': 'Uptown Funk - Bruno Mars', 'link': 'https://www.youtube.com/watch?v=OPf0YbXqDm0', 'type': 'youtube'},
                    {'title': 'September - Earth Wind & Fire', 'link': 'https://www.youtube.com/watch?v=Gs069dndIYk', 'type': 'youtube'},
                    {'title': 'Mr. Blue Sky - ELO', 'link': 'https://www.youtube.com/watch?v=wuJIqmha2Hc', 'type': 'youtube'}
                ],
                'description': 'Musik fun yang match energi kejutanmu! ✨'
            },
            'food': {
                'items': [
                    {'title': 'Sushi / Japanese 🍱', 'link': 'https://www.google.com/maps/search/sushi+near+me', 'description': 'Makanan dengan variasi rasa unik'},
                    {'title': 'Fusion Food 🌍', 'link': 'https://www.google.com/maps/search/fusion+restaurant+near+me', 'description': 'Coba rasa baru yang belum pernah kamu coba'},
                    {'title': 'Unique Snacks 🍿', 'link': 'https://www.google.com/maps/search/snack+shop+near+me', 'description': 'Camilan unik untuk mood penasaran'}
                ],
                'description': 'Makanan adventurous untuk mood penasaranmu! 🎉'
            },
            'activity': {
                'items': [
                    'Coba resep makanan baru yang belum pernah dibuat 👨‍🍳',
                    'Eksplorasi spot baru di kotamu 🗺️',
                    'Mulai hobby atau skill baru 🎨',
                    'Watch plot twist movies 🎬',
                    'Random act of kindness ke orang lain 💝'
                ],
                'description': 'Embrace the unexpected dengan aktivitas baru! 🌟'
            }
        },
        'Disgust': {
            'music': {
                'items': [
                    {'title': 'Here Comes the Sun - Beatles', 'link': 'https://www.youtube.com/watch?v=KQetemT1sWc', 'type': 'youtube'},
                    {'title': 'Three Little Birds - Bob Marley', 'link': 'https://www.youtube.com/watch?v=zaGUr6wzyT8', 'type': 'youtube'},
                    {'title': 'Lovely Day - Bill Withers', 'link': 'https://www.youtube.com/watch?v=bEeaS6fuUoA', 'type': 'youtube'}
                ],
                'description': 'Musik refreshing untuk cleanse the mind 🌿'
            },
            'food': {
                'items': [
                    {'title': 'Fresh Juice/Mojito 🍋', 'link': 'https://www.google.com/maps/search/fresh+juice+near+me', 'description': 'Minuman segar asam manis'},
                    {'title': 'Salad & Fruits 🥗', 'link': 'https://www.google.com/maps/search/salad+bar+near+me', 'description': 'Makanan bersih dan segar'},
                    {'title': 'Minty/Herbal Tea 🍃', 'link': 'https://www.google.com/maps/search/tea+shop+near+me', 'description': 'Pembersih palet rasa yang efektif'}
                ],
                'description': 'Makanan clean & fresh untuk reset senses! 💚'
            },
            'activity': {
                'items': [
                    'Bersih-bersih dan organize ruangan 🧹',
                    'Mandi dengan aromatherapy 🛁',
                    'Ganti sheets dan buka jendela untuk udara segar 🪟',
                    'Declutter - buang barang yang ga diperlukan 📦',
                    'Tonton comedy atau konten wholesome 😄'
                ],
                'description': 'Aktivitas cleansing untuk refresh mind & space! ✨'
            }
        },
        'Neutral': {
            'music': {
                'items': [
                    {'title': 'Weightless - Marconi Union', 'link': 'https://www.youtube.com/watch?v=UfcAVejslrU', 'type': 'youtube'},
                    {'title': 'Clair de Lune - Debussy', 'link': 'https://www.youtube.com/watch?v=CvFH_6DNRCY', 'type': 'youtube'},
                    {'title': 'River Flows in You - Yiruma', 'link': 'https://www.youtube.com/watch?v=7maJOI3QMu0', 'type': 'youtube'}
                ],
                'description': 'Musik ambient untuk maintain keseimbangan 🎵'
            },
            'food': {
                'items': [
                    {'title': 'Balanced Meal (Rice/Noodles) 🍚', 'link': 'https://www.google.com/maps/search/restaurant+near+me', 'description': 'Makanan sehari-hari yang seimbang'},
                    {'title': 'Sandwich/Toast 🥪', 'link': 'https://www.google.com/maps/search/sandwich+shop+near+me', 'description': 'Praktis dan mengenyangkan'},
                    {'title': 'Coffee/Tea Break ☕', 'link': 'https://www.google.com/maps/search/coffee+shop+near+me', 'description': 'Temani waktu santaimu'}
                ],
                'description': 'Makanan seimbang untuk energi stabil 🌾'
            },
            'activity': {
                'items': [
                    'Jalan santai atau light exercise 🚶',
                    'Baca buku atau artikel menarik 📚',
                    'Explore hobby baru yang menarik 🎨',
                    'Meditation atau mindfulness practice 🧘',
                    'Organize to-do list atau planning 📝'
                ],
                'description': 'Aktivitas balanced untuk hari yang tenang 🌤️'
            }
        }
    }
    
    @staticmethod
    def get_recommendations(emotion: str, category: str) -> Dict:
        """
        Get recommendations based on emotion and category
        (Auto-formatted to match Pydantic Schema)
        """
        # Ambil data mentah dari dictionary
        emotion_recs = RecommendationService.RECOMMENDATIONS.get(
            emotion,
            RecommendationService.RECOMMENDATIONS['Neutral']
        )
        
        # Ambil kategori spesifik (music/food/activity)
        category_data = emotion_recs.get(category, emotion_recs.get('music', {}))
        raw_items = category_data.get('items', [])
        
        formatted_items = []
        
        # PROSES FORMATTING DATA (PENTING!)
        for item in raw_items:
            # Jika item cuma string (kasus Activity), kita ubah jadi object
            if isinstance(item, str):
                formatted_items.append({
                    "title": item,
                    "description": "Aktivitas rekomendasi untukmu", # Deskripsi default
                    "type": category,
                    "link": None,
                    "image": None
                })
            # Jika item sudah object (kasus Music/Food)
            elif isinstance(item, dict):
                # Pastikan field description ada
                desc = item.get('description', category_data.get('description', ''))
                
                formatted_items.append({
                    "title": item.get('title', 'Unknown'),
                    "description": desc,
                    "type": category, # Tambahkan type secara eksplisit
                    "link": item.get('link'),
                    "image": item.get('image') # Opsional
                })

        return {
            'emotion': emotion,
            'category': category,
            'items': formatted_items, # Kirim item yang sudah rapi
            'description': category_data.get('description', '')
        }
    
    @staticmethod
    def track_click(
        emotion: str,
        category: str,
        title: str,
        session_id: str,
        emotion_log_id: str,
        db: Session
    ):
        """Track recommendation click"""
        
        # ✅ FIX: Handle empty string or None
        valid_emotion_log_id = None
        if emotion_log_id and emotion_log_id.strip():  # Check not empty
            try:
                valid_emotion_log_id = uuid.UUID(emotion_log_id)  # Validate UUID
            except (ValueError, AttributeError):
                print(f"Invalid UUID: {emotion_log_id}, setting to None")
                valid_emotion_log_id = None
        
        click = RecommendationClick(
            emotion_log_id=valid_emotion_log_id,  # ← Use validated UUID or None
            session_id=session_id,
            emotion=emotion,
            recommendation_type=category,
            recommendation_title=title
        )
        
        db.add(click)
        db.commit()
        
        return {"status": "tracked"}
    
    @staticmethod
    def get_popular_recommendations(
        db: Session,
        emotion: str = None,
        category: str = None,
        limit: int = 10
    ):
        """Get most popular recommendations"""
        from sqlalchemy import func
        
        query = db.query(
            RecommendationClick.emotion,
            RecommendationClick.recommendation_type,
            RecommendationClick.recommendation_title,
            func.count(RecommendationClick.id).label('clicks')
        )
        
        if emotion:
            query = query.filter(RecommendationClick.emotion == emotion)
        
        if category:
            query = query.filter(RecommendationClick.recommendation_type == category)
        
        return query.group_by(
            RecommendationClick.emotion,
            RecommendationClick.recommendation_type,
            RecommendationClick.recommendation_title
        ).order_by(func.count(RecommendationClick.id).desc()).limit(limit).all()