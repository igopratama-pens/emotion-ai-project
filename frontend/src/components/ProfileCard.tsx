import { Mail, Linkedin, Instagram } from "lucide-react";

interface ProfileCardProps {
  name: string;
  nim: string;
  image: string;
  email?: string;
  linkedin?: string;
  instagram?: string;
}

const ProfileCard = ({ name, nim, image, email, linkedin, instagram }: ProfileCardProps) => {
  return (
    <div className="bg-secondary rounded-xl p-6 shadow-md hover:shadow-lg transition-all hover:scale-105 duration-300">
      <div className="flex flex-col items-center">
        <div className="w-32 h-32 rounded-full overflow-hidden mb-4 border-4 border-primary-foreground shadow-lg">
          <img
            src={image}
            alt={name}
            className="w-full h-full object-cover"
          />
        </div>
        <h3 className="text-xl font-bold text-secondary-foreground mb-1">{name}</h3>
        <p className="text-sm text-secondary-foreground/80 mb-4">{nim}</p>
        <div className="flex gap-4">
          {email && (
            <a
              href={`mailto:${email}`}
              className="w-10 h-10 bg-primary-foreground rounded-full flex items-center justify-center hover:scale-110 transition-transform"
            >
              <Mail className="w-5 h-5 text-secondary" />
            </a>
          )}
          {linkedin && (
            <a
              href={linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 bg-primary-foreground rounded-full flex items-center justify-center hover:scale-110 transition-transform"
            >
              <Linkedin className="w-5 h-5 text-secondary" />
            </a>
          )}
          {instagram && (
            <a
              href={instagram}
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 bg-primary-foreground rounded-full flex items-center justify-center hover:scale-110 transition-transform"
            >
              <Instagram className="w-5 h-5 text-secondary" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfileCard;
