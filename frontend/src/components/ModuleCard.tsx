import { LucideIcon } from "lucide-react";

interface ModuleCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
}

const ModuleCard = ({ title, description, icon: Icon }: ModuleCardProps) => {
  return (
    <div className="bg-card rounded-xl p-6 shadow-md hover:shadow-lg transition-all hover:scale-105 duration-300 border border-border">
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 bg-secondary rounded-lg flex items-center justify-center flex-shrink-0">
          <Icon className="w-7 h-7 text-secondary-foreground" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-foreground mb-2">{title}</h3>
          <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
        </div>
      </div>
    </div>
  );
};

export default ModuleCard;
