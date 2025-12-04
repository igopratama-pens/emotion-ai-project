import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  // Konfigurasi untuk Local Development (npm run dev)
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  // ✅ KONFIGURASI BARU UNTUK RAILWAY (npm run preview)
  preview: {
    host: true, // Wajib true agar bisa diakses publik
    port: 8080, // Port standar untuk preview
    allowedHosts: [
      "lucky-nurturing-production.up.railway.app" // Domain kamu didaftarkan disini
    ]
  }
})