import api from './api';

export interface AdminLoginRequest {
  username: string;
  password: string;
}

export interface AdminLoginResponse {
  access_token: string;
  username: string;
  email: string;
}

export interface DashboardStats {
  total_users?: number;
  total_emotions?: number;
  recent_activity?: any[];
  total_detections?: number;
  unique_sessions?: number;
  total_messages?: number;
  total_clicks?: number;
  most_common_emotion?: string;
  trends?: {
    detections: string;
    sessions: string;
    messages: string;
    clicks: string;
  };
}

export interface EmotionStats {
  emotion: string;
  count: number;
  percentage?: number;
}

// LOGIN
export const adminLogin = async (credentials: AdminLoginRequest): Promise<AdminLoginResponse> => {
  const params = new URLSearchParams();
  params.append('username', credentials.username);
  params.append('password', credentials.password);

  const response = await api.post<any>('/api/admin/login', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  
  if (response.data.access_token) {
    localStorage.setItem('admin_token', response.data.access_token);
    localStorage.setItem('admin_user', JSON.stringify({
      username: credentials.username,
      email: credentials.username 
    }));
  }
  return response.data;
};

export const adminLogout = (): void => {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
};

export const isAdminAuthenticated = (): boolean => {
  return !!localStorage.getItem('admin_token');
};

export const getAdminUser = (): any => {
  const user = localStorage.getItem('admin_user');
  return user ? JSON.parse(user) : null;
};

// DASHBOARD STATS
export const getDashboardStats = async (timeRange: string = '30d'): Promise<DashboardStats> => {
  try {
    const response = await api.get<DashboardStats>(`/api/admin/dashboard?time_range=${timeRange}`);
    return response.data;
  } catch (error) {
    console.error("Gagal load dashboard stats", error);
    return {};
  }
};

// ✅ FIX: Tambahkan parameter limit & hitung persentase agar tidak 0%
export const getEmotionStats = async (limit: number = 30): Promise<EmotionStats[]> => {
  try {
    const response = await api.get(`/api/emotion/stats?limit=${limit}`);
    const data = response.data;
    
    if (data.emotion_counts) {
      // 1. Hitung Total Semua Emosi untuk pembagi
      const total = Object.values(data.emotion_counts).reduce((acc: any, curr: any) => acc + Number(curr), 0) as number;

      // 2. Map data dan hitung %
      return Object.entries(data.emotion_counts).map(([emotion, count]) => ({
        emotion: emotion,
        count: Number(count),
        // Rumus Persentase: (Jumlah / Total) * 100
        percentage: total > 0 ? (Number(count) / total) * 100 : 0
      }));
    }
    return [];
  } catch (error) {
    return [];
  }
};