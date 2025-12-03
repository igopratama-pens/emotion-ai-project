import { Link, useLocation } from "react-router-dom";
import { User } from "lucide-react";

interface NavbarProps {
  variant?: "default" | "admin";
}

const Navbar = ({ variant = "default" }: NavbarProps) => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-primary shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3 hover:opacity-90 transition-opacity">
            <div className="w-10 h-10 rounded-full overflow-hidden">
              <img
                src="/icon.png"
                alt="Logo"
                className="h-9 w-9 object-contain rounded-full"
              />
            </div>
            <span className="text-xl font-bold text-primary-foreground">
              Emotion Detection
            </span>
          </Link>

          {variant === "default" && (
            <div className="flex items-center gap-8">
              <Link
                to="/"
                className={`text-primary-foreground hover:text-secondary transition-colors font-medium ${
                  isActive("/") ? "text-secondary" : ""
                }`}
              >
                Home
              </Link>
              <Link
                to="/about"
                className={`text-primary-foreground hover:text-secondary transition-colors font-medium ${
                  isActive("/about") ? "text-secondary" : ""
                }`}
              >
                About
              </Link>
              <Link
                to="/contact"
                className={`text-primary-foreground hover:text-secondary transition-colors font-medium ${
                  isActive("/contact") ? "text-secondary" : ""
                }`}
              >
                Contact
              </Link>
              <Link
                to="/admin/login"
                className="bg-secondary text-secondary-foreground px-5 py-2 rounded-lg hover:opacity-90 transition-opacity font-medium shadow-md"
              >
                Login
              </Link>
            </div>
          )}

          {variant === "admin" && (
            <Link
              to="/"
              className="bg-secondary text-secondary-foreground px-5 py-2 rounded-lg hover:opacity-90 transition-opacity font-medium shadow-md"
            >
              Logout
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
