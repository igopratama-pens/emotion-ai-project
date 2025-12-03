import ModuleCard from "@/components/ModuleCard";
import { Brain, Scan, Target, Eye, Activity, Cpu } from "lucide-react";

const About = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Navbar dihapus dari sini karena sudah ada di App.tsx */}
      
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto space-y-20">
          {/* Hero Section */}
          <div className="text-center space-y-4 animate-fade-in">
            <h1 className="text-5xl font-bold text-primary mb-4">
              Every expression has a story
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Kami menggunakan teknologi AI terdepan untuk memahami dan menganalisis emosi manusia
            </p>
          </div>

          {/* About This Project */}
          <section className="space-y-8">
            <h2 className="text-3xl font-bold text-primary text-center">About This Project</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <ModuleCard
                icon={Scan}
                title="Facial Feature Extraction"
                description="Mendeteksi dan mengekstrak fitur wajah utama menggunakan deep learning untuk analisis yang akurat."
              />
              <ModuleCard
                icon={Brain}
                title="Emotion Classification"
                description="Mengklasifikasikan emosi ke dalam 7 kategori: happy, sad, angry, fear, surprise, disgust, dan neutral."
              />
              <ModuleCard
                icon={Activity}
                title="Real-time Analysis"
                description="Analisis emosi secara real-time dengan performa tinggi dan akurasi yang optimal."
              />
            </div>
          </section>

          {/* Why This Technology */}
          <section className="space-y-8">
            <h2 className="text-3xl font-bold text-primary text-center">Why This Technology</h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-card rounded-xl p-8 shadow-md hover:shadow-lg transition-all border border-border text-center">
                <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mx-auto mb-4">
                  <Target className="w-8 h-8 text-secondary-foreground" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">Akurasi Tinggi</h3>
                <p className="text-muted-foreground">Model AI dengan tingkat akurasi &gt;90%</p>
              </div>
              <div className="bg-card rounded-xl p-8 shadow-md hover:shadow-lg transition-all border border-border text-center">
                <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mx-auto mb-4">
                  <Eye className="w-8 h-8 text-secondary-foreground" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">Easy to Use</h3>
                <p className="text-muted-foreground">Interface intuitif untuk semua pengguna</p>
              </div>
              <div className="bg-card rounded-xl p-8 shadow-md hover:shadow-lg transition-all border border-border text-center">
                <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mx-auto mb-4">
                  <Cpu className="w-8 h-8 text-secondary-foreground" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">Fast Processing</h3>
                <p className="text-muted-foreground">Deteksi dalam hitungan milidetik</p>
              </div>
            </div>
          </section>

          {/* Our Vision */}
          <section className="space-y-6 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-3xl p-12">
            <h2 className="text-3xl font-bold text-primary text-center">Our Vision</h2>
            <p className="text-lg text-foreground text-center max-w-3xl mx-auto leading-relaxed">
              Membangun teknologi yang dapat memahami emosi manusia untuk meningkatkan 
              interaksi manusia-komputer, mendukung kesehatan mental, dan menciptakan 
              pengalaman digital yang lebih empati dan personal.
            </p>
          </section>
        </div>
      </main>
    </div>
  );
};

export default About;