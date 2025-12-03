import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

MODEL_PATH = "app/ml/emotion_cnn_fixed.h5"

def check():
    print(f"🕵️‍♂️ Memeriksa Model: {MODEL_PATH}")
    
    if not os.path.exists(MODEL_PATH):
        print("❌ File model tidak ditemukan!")
        return

    try:
        # Load model
        model = keras.models.load_model(MODEL_PATH, compile=False)
        print("✅ Model berhasil dimuat.")
        
        # 1. Cek Weights Layer Pertama
        # Jika rata-ratanya 0 atau sangat kecil mendekati 0, berarti model kosong/reset
        first_layer_weights = model.layers[0].get_weights()
        if len(first_layer_weights) > 0:
            w = first_layer_weights[0]
            print(f"📊 Statistik Bobot Layer Pertama:")
            print(f"   - Mean: {w.mean():.6f}")
            print(f"   - Std : {w.std():.6f}")
            print(f"   - Min : {w.min():.6f}")
            print(f"   - Max : {w.max():.6f}")
            
            if w.std() < 0.0001:
                print("\n⚠️ PERINGATAN: Bobot model terlihat seperti inisialisasi random/kosong!")
                print("   Kemungkinan file model ini BUKAN hasil training yang benar.")
            else:
                print("\n✅ Bobot terlihat normal (bervariasi).")
        
        # 2. Test dengan RANDOM NOISE (Bukan gambar hitam)
        # Jika outputnya tetap 0.1428..., berarti model fix rusak.
        print("\n🧪 Testing dengan Input Random Noise...")
        img = np.random.rand(1, 100, 100, 3).astype('float32')
        pred = model.predict(img, verbose=0)[0]
        
        print(f"🎯 Hasil Prediksi: {pred}")
        
        is_uniform = np.allclose(pred, 0.14285715, atol=0.01)
        if is_uniform:
            print("\n❌ KESIMPULAN: MODEL RUSAK / KOSONG.")
            print("   Output flat (14.28%) meskipun inputnya random.")
            print("   Solusi: Anda harus mencari file .h5 yang BENAR dari backup.")
        else:
            print("\n✅ KESIMPULAN: MODEL HIDUP/RESPONSIF.")
            print("   Masalah sebelumnya hanya karena input gambar hitam.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check()