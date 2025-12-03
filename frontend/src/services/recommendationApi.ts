/**
 * ============================================================================
 * FIXED: recommendationApi.ts
 * ============================================================================
 */

import api from './api';

export interface Recommendation {
  type: 'music' | 'food' | 'activity';
  title: string;
  description: string;
  link?: string;
  image?: string;
  icon?: string;
}

export interface RecommendationResponse {
  emotion: string;
  music: Recommendation[];
  food: Recommendation[];
  activity: Recommendation[];
}

export interface RecommendationClickRequest {
  session_id: string;
  emotion_log_id?: string;
  emotion: string;
  category: string; // ✅ FIXED: Changed from "recommendation_type" to "category"
  title: string;    // ✅ FIXED: Changed from "recommendation_title" to "title"
}

/**
 * Get recommendations by emotion
 */
export const getRecommendations = async (
  emotion: string
): Promise<RecommendationResponse> => {
  // ✅ FIXED: Send as POST with body (sesuai backend router)
  const response = await api.post<RecommendationResponse>(
    '/api/recommendations/',
    { emotion }
  );
  return response.data;
};

/**
 * Track recommendation click
 */
export const trackRecommendationClick = async (
  data: RecommendationClickRequest
): Promise<void> => {
  // ✅ FIXED: Send to /track endpoint dengan field name yang benar
  const payload = {
    emotion: data.emotion,
    category: data.category,  // ← "category" not "recommendation_type"
    title: data.title,        // ← "title" not "recommendation_title"
    session_id: data.session_id,
    emotion_log_id: data.emotion_log_id || '',
  };

  await api.post('/api/recommendations/track', payload);
};

/**
 * Get top recommendations (admin only)
 */
export const getTopRecommendations = async (): Promise<
  Array<{
    emotion: string;
    category: string;
    title: string;
    click_count: number;
  }>
> => {
  const response = await api.get('/api/recommendations/popular');
  return response.data.popular || [];
};