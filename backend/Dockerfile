# 1. Gunakan Python 3.10 sebagai dasar
FROM python:3.10-slim

# 2. Install library sistem Linux yang hilang (Obat error libGL)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Buat folder kerja di dalam server
WORKDIR /app

# 4. Copy daftar library python kamu
COPY requirements.txt .

# 5. Install library python (FastAPI, TensorFlow, dll)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy semua kodingan backend kamu
COPY . .

# 7. Perintah untuk menyalakan server saat deploy selesai
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}