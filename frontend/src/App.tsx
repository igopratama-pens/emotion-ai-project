/**
 * Main App Component - WITH CONTEXT PROVIDERS
 */

/**
 * Main App Component - WITH CONTEXT PROVIDERS
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from '@/components/ui/toaster';

// Context Providers
import { AuthProvider } from '@/context/AuthContext';
import { EmotionProvider } from '@/context/EmotionContext';
import { ChatProvider } from '@/context/ChatContext';

// Pages
import Home from '@/pages/Home';
import Detect from '@/pages/Detect';
import About from '@/pages/About';
import Contact from '@/pages/Contact';
import AdminLogin from '@/pages/AdminLogin';
import Dashboard from '@/pages/Dashboard';
import NotFound from '@/pages/NotFound';

// Layout
import Navbar from '@/components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <EmotionProvider>
          <ChatProvider>
            <div className="min-h-screen">
              <Routes>
                {/* Public Routes - with Navbar */}
                <Route path="/" element={<><Navbar /><Home /></>} />
                <Route path="/detect" element={<><Navbar /><Detect /></>} />
                <Route path="/about" element={<><Navbar /><About /></>} />
                <Route path="/contact" element={<><Navbar /><Contact /></>} />

                {/* Admin Routes - without Navbar */}
                <Route path="/admin/login" element={<AdminLogin />} />
                <Route path="/admin/dashboard" element={<Dashboard />} />

                {/* Fallback */}
                <Route path="*" element={<NotFound />} />
              </Routes>

              {/* Toast Notifications */}
              <Toaster />
            </div>
          </ChatProvider>
        </EmotionProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;