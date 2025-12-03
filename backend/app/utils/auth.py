from passlib.context import CryptContext

# Konfigurasi hashing password menggunakan bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Memeriksa apakah password plain cocok dengan hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Mengubah password plain menjadi hash"""
    return pwd_context.hash(password)