import h5py
import shutil
import os

# Path file (Pastikan Anda menjalankan script ini dari folder 'backend')
original_model = "app/ml/emotion_cnn.h5"
fixed_model = "app/ml/emotion_cnn_fixed.h5"

print(f"🔧 Memulai perbaikan model (Direct H5 Patch)...")
print(f"📂 Mencari file asal di: {original_model}")

# Cek apakah file asli ada
if not os.path.exists(original_model):
    print(f"❌ ERROR: File '{original_model}' tidak ditemukan!")
    print("👉 Pastikan Anda sudah copy file 'emotion_cnn.h5' dari app_lama ke folder 'backend/app/ml/'")
    exit()

# 1. Duplikat file (Backup agar file asli aman)
print("📋 Menduplikasi file...")
shutil.copyfile(original_model, fixed_model)
print(f"✅ File tersalin ke: {fixed_model}")

# 2. Buka file baru dan Ganti Teks Config-nya
try:
    with h5py.File(fixed_model, 'r+') as f:
        if 'model_config' in f.attrs:
            # Ambil config (biasanya dalam format bytes json)
            config = f.attrs['model_config']
            
            # Decode bytes ke string
            if isinstance(config, bytes):
                config_str = config.decode('utf-8')
            else:
                config_str = str(config)

            # --- BAGIAN BEDAH ---
            # Mengganti 'batch_shape' (lama) menjadi 'batch_input_shape' (baru)
            if 'batch_shape' in config_str:
                print("⚠️  Ditemukan keyword lawas: 'batch_shape'")
                new_config = config_str.replace('"batch_shape":', '"batch_input_shape":')
                
                # Encode balik ke bytes dan simpan
                f.attrs['model_config'] = new_config.encode('utf-8')
                print("✅ BERHASIL: Config diperbarui ke 'batch_input_shape'")
            else:
                print("ℹ️  Info: Keyword 'batch_shape' tidak ditemukan. Model mungkin sudah format baru atau beda masalah.")
        else:
            print("❌ Warning: Atribut 'model_config' tidak ditemukan di dalam file h5.")

    print("-" * 30)
    print(f"🎉 SELESAI! Model 'fixed' siap digunakan.")
    print(f"📍 Lokasi: {fixed_model}")

except Exception as e:
    print(f"❌ Error saat memproses file h5: {e}")