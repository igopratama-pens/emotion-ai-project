import ProfileCard from "@/components/ProfileCard";

const Contact = () => {
  const teamMembers = [
    {
      name: "Muhammad Igo Pratama",
      nim: "3323600031",
      image: "igo.png",
      email: "ahmad.rizki@example.com",
      linkedin: "https://linkedin.com",
      instagram: "https://instagram.com",
    },
    {
      name: "Al Rahma Dinda S.",
      nim: "3323600038",
      image: "/din.png",
      email: "siti.nur@example.com",
      linkedin: "https://linkedin.com",
      instagram: "https://instagram.com",
    },
    {
      name: "Evinda Eka Ayudia L.",
      nim: "3323600039",
      image: "/vin.png",
      email: "budi.santoso@example.com",
      linkedin: "https://linkedin.com",
      instagram: "https://instagram.com",
    },
    {
      name: "Nur Aghni Rizqiyah B.",
      nim: "3323600058",
      image: "/mi.png",
      email: "dewi.lestari@example.com",
      linkedin: "https://linkedin.com",
      instagram: "https://instagram.com",
    },
    {
      name: "R.Aj Maria Shovia F",
      nim: "3323600059",
      image: "/vi.png",
      email: "eko.prasetyo@example.com",
      linkedin: "https://linkedin.com",
      instagram: "https://instagram.com",
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar dihapus dari sini karena sudah ada di App.tsx */}
      
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto space-y-12">
          <div className="text-center space-y-4 animate-fade-in">
            <h1 className="text-5xl font-bold text-primary">Contact Our Team</h1>
            <p className="text-xl text-muted-foreground">
              Hubungi tim kami untuk pertanyaan, kolaborasi, atau feedback
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-8">
            {teamMembers.map((member, index) => (
              <div
                key={index}
                className="animate-slide-up w-[300px]"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <ProfileCard {...member} />
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Contact;