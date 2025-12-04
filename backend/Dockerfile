# 1. Gunakan Base Image Python 3.10 (Versi Slim agar ringan)
FROM python:3.10-slim

# 2. Install System Dependencies (UPDATE FIX)
# 'libgl1-mesa-glx' diganti jadi 'libgl1' karena versi lama sudah deprecated
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Set Working Directory
WORKDIR /app

# 4. Copy Requirements dulu
COPY requirements.txt .

# 5. Install Python Dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy seluruh kode aplikasi
COPY . .

# 7. Perintah untuk menjalankan aplikasi
# Menggunakan variabel PORT dari Railway
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}