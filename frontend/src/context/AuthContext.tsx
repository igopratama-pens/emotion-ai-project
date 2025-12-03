/**
 * Auth Context for Admin Authentication
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  adminLogin as apiAdminLogin,
  adminLogout as apiAdminLogout,
  isAdminAuthenticated,
  getAdminUser,
  AdminLoginRequest,
} from '../services/adminApi';

interface AdminUser {
  username: string;
  email: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: AdminUser | null;
  login: (credentials: AdminLoginRequest) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<AdminUser | null>(null);
  const [loading, setLoading] = useState(true);

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = () => {
      const authenticated = isAdminAuthenticated();
      setIsAuthenticated(authenticated);
      
      if (authenticated) {
        const userData = getAdminUser();
        setUser(userData);
      }
      
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (credentials: AdminLoginRequest) => {
    try {
      const response = await apiAdminLogin(credentials);
      setIsAuthenticated(true);
      setUser({
        username: response.username,
        email: response.email,
      });
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };

  const logout = () => {
    apiAdminLogout();
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        login,
        logout,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};