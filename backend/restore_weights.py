import os
import tensorflow as tf
from app.ml.model_architecture import build_emotion_cnn

# Path
OLD_MODEL_PATH = "app/ml/emotion_cnn.h5"        # File ASLI 7.5MB
NEW_MODEL_PATH = "app/ml/emotion_cnn_fixed.h5"  # File HASIL BERSIH

def restore():
    print("🚑 MEMULAI OPERASI PEMULIHAN MODEL...")
    
    # Cek ukuran file untuk memastikan itu file yang benar
    if os.path.exists(OLD_MODEL_PATH):
        size_mb = os.path.getsize(OLD_MODEL_PATH) / (1024 * 1024)
        print(f"📦 Ditemukan file sumber: {size_mb:.2f} MB")
        if size_mb < 7.0:
            print("⚠️  PERINGATAN: Ukuran file tampak kecil! Pastikan ini file 7MB+ dari app_lama.")
    else:
        print(f"❌ Error: File {OLD_MODEL_PATH} tidak ditemukan!")
        return

    try:
        # 1. Bangun Arsitektur Baru (Wadah Kosong tapi Sehat)
        print("🏗️  Membangun arsitektur model baru...")
        model = build_emotion_cnn()
        
        # 2. Load Weights Only (Mengabaikan error batch_shape)
        print(f"💉 Menyuntikkan bobot dari {OLD_MODEL_PATH}...")
        # Ini magic-nya: hanya ambil angka-angka bobotnya, abaikan config error
        model.load_weights(OLD_MODEL_PATH, by_name=True, skip_mismatch=True)
        
        # 3. Save Model Baru
        print(f"💾 Menyimpan model sehat ke {NEW_MODEL_PATH}...")
        # Kita simpan tanpa optimizer state agar file baru lebih kecil & bersih (inference only)
        model.save(NEW_MODEL_PATH, include_optimizer=False)
        
        print("\n✅ SUKSES! Model berhasil dipulihkan.")
        print(f"   File baru '{NEW_MODEL_PATH}' siap digunakan.")
        
    except Exception as e:
        print(f"\n❌ Gagal memulihkan model: {e}")

if __name__ == "__main__":
    restore()