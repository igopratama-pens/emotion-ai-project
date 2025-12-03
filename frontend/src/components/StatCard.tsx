import { LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/card";

interface StatCardProps {
  title: string;
  // ✅ FIX: Menerima string atau number agar tidak error saat dikirim angka 0
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  // ✅ FIX: Menerima string bebas agar "blue", "green" dsb valid
  color?: string; 
}

const StatCard = ({ title, value, icon: Icon, trend, color = "gray" }: StatCardProps) => {
  
  // Mapping warna untuk styling
  const colorStyles: Record<string, string> = {
    blue: "bg-blue-100 text-blue-600",
    green: "bg-green-100 text-green-600",
    purple: "bg-purple-100 text-purple-600",
    orange: "bg-orange-100 text-orange-600",
    red: "bg-red-100 text-red-600",
    gray: "bg-gray-100 text-gray-600",
    primary: "bg-primary/10 text-primary",
    secondary: "bg-secondary text-secondary-foreground",
  };

  // Fallback ke gray jika warna tidak ditemukan
  const activeColorClass = colorStyles[color] || colorStyles.gray;

  return (
    <Card className="p-6 hover:shadow-md transition-shadow border border-border">
      <div className="flex items-start justify-between mb-4">
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${activeColorClass}`}>
          <Icon className="w-6 h-6" />
        </div>
        {trend && (
          <span className="text-sm text-muted-foreground bg-secondary px-2 py-1 rounded-full">
            {trend}
          </span>
        )}
      </div>
      <div>
        <h3 className="text-sm font-medium text-muted-foreground mb-1">{title}</h3>
        <p className="text-3xl font-bold text-foreground">{value}</p>
      </div>
    </Card>
  );
};

export default StatCard;