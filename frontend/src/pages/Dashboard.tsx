/**
 * Admin Dashboard - CLEAN & FIXED
 */

import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/context/AuthContext';
import StatCard from '@/components/StatCard';
import {
  getDashboardStats,
  getEmotionStats,
  DashboardStats,
  EmotionStats,
} from '@/services/adminApi';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Users, Brain, MessageSquare, MousePointer, LogOut, RefreshCw } from 'lucide-react';

const EMOTION_COLORS: Record<string, string> = {
  Happiness: '#FCD34D',
  Sadness: '#60A5FA',
  Anger: '#EF4444',
  Fear: '#A78BFA',
  Surprise: '#FB923C',
  Disgust: '#34D399',
  Neutral: '#9CA3AF',
};

export default function Dashboard() {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { isAuthenticated, user, logout, loading: authLoading } = useAuth();

  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [emotionStats, setEmotionStats] = useState<EmotionStats[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate('/admin/login');
    }
  }, [isAuthenticated, authLoading, navigate]);

  useEffect(() => {
    if (isAuthenticated) {
      loadDashboardData();
    }
  }, [isAuthenticated]);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // ✅ FIX: Hapus getActivityLogs dari sini agar tidak error merah
      const [statsData, emotionData] = await Promise.all([
        getDashboardStats(),
        getEmotionStats(30),
      ]);

      setStats(statsData);
      setEmotionStats(emotionData);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      toast({
        title: 'Error',
        description: 'Gagal memuat data dashboard',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
    toast({
      title: 'Logout Berhasil',
      description: 'Anda telah keluar dari dashboard',
    });
  };

  if (authLoading || loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
              {user && (
                <p className="text-sm text-gray-600 mt-1">
                  Welcome, {user.username}
                </p>
              )}
            </div>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={loadDashboardData}
                disabled={loading}
              >
                <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              <Button variant="destructive" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Detections"
            value={stats?.total_detections || 0}
            icon={Brain}
            color="blue"
          />
          <StatCard
            title="Unique Sessions"
            value={stats?.unique_sessions || 0}
            icon={Users}
            color="green"
          />
          <StatCard
            title="Total Messages"
            value={stats?.total_messages || 0}
            icon={MessageSquare}
            color="purple"
          />
          <StatCard
            title="Recommendation Clicks"
            value={stats?.total_clicks || 0}
            icon={MousePointer}
            color="orange"
          />
        </div>

        {/* Most Common Emotion Badge */}
        {stats?.most_common_emotion && (
          <Card className="p-4 mb-8">
            <div className="flex items-center justify-between">
              <span className="text-gray-600 font-medium">Most Common Emotion:</span>
              <span
                className="px-4 py-2 rounded-full text-white font-bold"
                style={{ backgroundColor: EMOTION_COLORS[stats.most_common_emotion] }}
              >
                {stats.most_common_emotion}
              </span>
            </div>
          </Card>
        )}

        {/* Charts */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          {/* Emotion Distribution - Bar Chart */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Emotion Distribution (Last 30 Days)</h3>
            {emotionStats.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={emotionStats}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="emotion" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#4285F4" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-gray-400">
                No data available
              </div>
            )}
          </Card>

          {/* Emotion Distribution - Pie Chart */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Emotion Percentage</h3>
            {emotionStats.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={emotionStats}
                    dataKey="count"
                    nameKey="emotion"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={(entry) => `${entry.emotion}: ${entry.percentage?.toFixed(1)}%`}
                  >
                    {emotionStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={EMOTION_COLORS[entry.emotion] || '#9CA3AF'} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-gray-400">
                No data available
              </div>
            )}
          </Card>
        </div>

        {/* ✅ Recent Activity telah dihapus dari sini */}
        
      </main>
    </div>
  );
}