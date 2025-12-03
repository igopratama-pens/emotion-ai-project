import sys
import os
from sqlalchemy import text

# Pastikan bisa import modul app
sys.path.append(os.getcwd())

from app.database import SessionLocal

def reset_data():
    print("🧹 MEMULAI PEMBERSIHAN DASHBOARD...")
    db = SessionLocal()
    
    try:
        # 1. Hapus Log Emosi
        print("   🗑️  Menghapus riwayat emosi...")
        db.execute(text("DELETE FROM emotion_logs"))
        
        # 2. Hapus Log Chat
        print("   🗑️  Menghapus riwayat chat...")
        db.execute(text("DELETE FROM chat_logs"))
        
        # 3. Hapus Log Klik Rekomendasi
        print("   🗑️  Menghapus riwayat klik...")
        db.execute(text("DELETE FROM recommendation_clicks"))
        
        # Commit perubahan
        db.commit()
        print("\n✅ SUKSES! Dashboard sudah bersih (0).")
        print("   Catatan: Akun Admin TIDAK dihapus, jadi kamu bisa langsung login.")
        
    except Exception as e:
        print(f"\n❌ Gagal mereset data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Konfirmasi keamanan
    confirm = input("⚠️  Yakin ingin menghapus SEMUA data di dashboard? (y/n): ")
    if confirm.lower() == 'y':
        reset_data()
    else:
        print("Operasi dibatalkan.")