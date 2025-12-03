"""
Script Test Gambar Asli (Happy/Sad/Neutral)
Untuk memvalidasi preprocessing dan prediksi model.
"""
import cv2
import numpy as np
import os
import sys

# Memastikan modul app bisa dibaca
sys.path.append(os.getcwd())

from app.ml.model_loader import emotion_model
from app.utils.face_detection import detect_and_crop_face
from app.utils.image_processing import preprocess_for_model
from app.config import settings

def run_test():
    print("🚀 Memulai Test Deteksi Emosi...")
    
    # 1. Load Model
    try:
        emotion_model.load_model()
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Gagal load model: {e}")
        return

    # 2. Daftar file test
    TEST_IMAGES = [
        "test_happy.jpg", 
        "test_sad.jpg",    
        "test_neutral.jpg" 
    ]

    for img_path in TEST_IMAGES:
        print("\n" + "="*60)
        print(f"📸 Testing File: {img_path}")
        print("="*60)
        
        # Cek file ada atau tidak
        if not os.path.exists(img_path):
            print(f"❌ File tidak ditemukan: {img_path}")
            print("   (Pastikan file ada di folder backend/)")
            continue
        
        # Load image
        img = cv2.imread(img_path)
        if img is None:
            print(f"❌ Gagal membaca gambar (format rusak/tidak support)")
            continue
            
        print(f"✅ Image loaded. Dimensi asli: {img.shape}")
        
        # Step 1: Face detection & Crop
        face, detected = detect_and_crop_face(img)
        print(f"\n🔍 Face Detection:")
        print(f"   Detected: {detected}")
        print(f"   Face Crop Shape: {face.shape}")
        
        # Simpan hasil crop untuk diperiksa mata manusia
        debug_filename = f"debug_crop_{img_path}"
        cv2.imwrite(debug_filename, face)
        print(f"   💾 Hasil crop disimpan ke: {debug_filename}")
        print("   (Cek file ini! Apakah wajah terpotong dengan benar?)")
        
        # Step 2: Preprocessing (Resize & Normalize)
        preprocessed = preprocess_for_model(face)
        print(f"\n⚙️ Preprocessing:")
        print(f"   Output Shape: {preprocessed.shape}")
        print(f"   Value Range: [{preprocessed.min():.4f} - {preprocessed.max():.4f}]")
        
        # Step 3: Prediction
        emotion, confidence, probs = emotion_model.predict(preprocessed)
        
        print(f"\n🎯 HASIL PREDIKSI:")
        print(f"   Emosi: {emotion.upper()}")
        print(f"   Confidence: {confidence:.2%}")
        
        print(f"\n📊 Detail Probabilitas:")
        emotions_list = list(settings.EMOTIONS.values())
        
        for i, val in enumerate(probs):
            emo_label = emotions_list[i]
            bar_len = int(val * 20)
            bar = "█" * bar_len
            print(f"   {emo_label:10s}: {val:.4f}  {bar}")
        
        # Cek Indikasi Model Rusak (Uniform Output)
        if np.allclose(probs, 1/7, atol=0.01):
            print("\n⚠️ WARNING: Output Uniform (14.28%). Model mungkin rusak atau preprocessing salah!")

if __name__ == "__main__":
    run_test()