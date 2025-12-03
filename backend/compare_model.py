import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Path model
ORIGINAL_MODEL = "app/ml/emotion_cnn.h5"
FIXED_MODEL = "app/ml/emotion_cnn_fixed.h5"

def compare():
    print("🔍 Membandingkan Model Asli vs Fixed...")

    # 1. Buat Dummy Image (Hitam) ukuran 100x100
    # Kita pakai dummy biar cepat, tujuannya cuma lihat output angka
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img_batch = np.expand_dims(img.astype('float32') / 255.0, axis=0)

    # 2. Load Model Fixed (Yang sedang dipakai sekarang)
    print(f"Loading Fixed Model: {FIXED_MODEL}")
    try:
        model_fixed = keras.models.load_model(FIXED_MODEL, compile=False)
        pred_fixed = model_fixed.predict(img_batch, verbose=0)[0]
        print(f"✅ Prediksi Fixed: {pred_fixed}")
    except Exception as e:
        print(f"❌ Gagal load Fixed: {e}")
        return

    # 3. Load Model Asli (Pakai trik khusus untuk bypass error batch_shape)
    print(f"Loading Original Model: {ORIGINAL_MODEL}")
    try:
        # Trik: Load sebagai h5py dulu untuk bypass config, lalu load weights (Simulasi Solusi B)
        # Tapi karena kita belum punya arsitektur, kita coba load paksa dengan opsi khusus
        model_orig = keras.models.load_model(ORIGINAL_MODEL, compile=False)
        pred_orig = model_orig.predict(img_batch, verbose=0)[0]
        print(f"✅ Prediksi Asli : {pred_orig}")
        
        # Bandingkan
        diff = np.abs(pred_fixed - pred_orig).sum()
        print("\n" + "="*30)
        print(f"SELISIH PREDIKSI: {diff:.10f}")
        if diff > 0.0001:
            print("⚠️  HASIL BEDA! File Fixed telah merusak akurasi.")
        else:
            print("✅ Hasil identik. Masalah bukan di file model.")
            
    except Exception as e:
        print(f"⚠️ Tidak bisa load model asli secara langsung karena error versi: {e}")
        print("Kesimpulan: Kita WAJIB pakai Solusi B (Rebuild Arsitektur).")

if __name__ == "__main__":
    compare()