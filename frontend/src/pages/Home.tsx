import { Link } from "react-router-dom";
// HAPUS import Navbar karena sudah ada di App.tsx
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

const Home = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* <Navbar />  <-- INI DIHAPUS SUPAYA TIDAK GANDA */}
      
      <main className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 gap-12 items-center min-h-[calc(100vh-200px)]">
          
          {/* Bagian Kiri: Teks */}
          <div className="space-y-8 animate-slide-up">
            <h1 className="text-5xl md:text-6xl font-bold text-primary leading-tight">
              Emotion Detection
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed">
              Teknologi canggih untuk mendeteksi dan menganalisis emosi manusia secara real-time 
              menggunakan AI dan Computer Vision yang akurat.
            </p>
            <div className="flex gap-4">
              <Link to="/detect">
                <Button size="lg" className="bg-secondary hover:bg-secondary/90 text-secondary-foreground font-medium shadow-lg">
                  Get Started!
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
              <Link to="/about">
                <Button size="lg" variant="outline" className="font-medium">
                  Learn More
                </Button>
              </Link>
            </div>
          </div>

          {/* Bagian Kanan: Gambar */}
          <div className="relative animate-fade-in">
            <div className="flex items-center justify-center">
              {/* Pastikan file 'home.png' ada di folder 'frontend/public/' */}
              <img
                src="/home.png" 
                alt="Emotion Detection"
                className="w-full max-w-3xl object-contain drop-shadow-xl"
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;