from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.admin import Admin
# Menggunakan auth.py yang baru saja dibuat
from app.utils.auth import get_password_hash 
import sys

# Pastikan table sudah dibuat (penting jika database masih kosong)
from app.models import admin
admin.Base.metadata.create_all(bind=engine)

def create_admin_user(username, email, password):
    db = SessionLocal()
    try:
        # 1. Cek apakah username sudah ada
        existing_user = db.query(Admin).filter(Admin.username == username).first()
        if existing_user:
            print(f"❌ User dengan username '{username}' sudah ada!")
            return

        # 2. Cek apakah email sudah ada
        existing_email = db.query(Admin).filter(Admin.email == email).first()
        if existing_email:
            print(f"❌ User dengan email '{email}' sudah ada!")
            return

        # 3. Buat user baru
        # PERBAIKAN: Menggunakan 'password_hash' sesuai model, bukan 'hashed_password'
        hashed_pwd = get_password_hash(password)
        
        new_admin = Admin(
            username=username, 
            email=email, 
            password_hash=hashed_pwd
        )
        
        db.add(new_admin)
        db.commit()
        print(f"✅ Sukses! Admin user '{username}' berhasil dibuat.")
        
    except Exception as e:
        print(f"❌ Terjadi Error Database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("\n--- Script Pembuatan Admin ---")
    try:
        u_name = input("Masukkan Username: ").strip()
        u_email = input("Masukkan Email: ").strip()
        p_word = input("Masukkan Password: ").strip()
        
        if u_name and p_word and u_email:
            create_admin_user(u_name, u_email, p_word)
        else:
            print("❌ Error: Username, Email, dan Password tidak boleh kosong.")
    except KeyboardInterrupt:
        print("\nOperasi dibatalkan.")