/**
 * Emotion Detection API Service
 */

import api from './api';

export interface EmotionDetectionRequest {
  image: string; // Base64 encoded image
  session_id?: string;
}

export interface EmotionDetectionResponse {
  emotion: string;
  confidence: number;
  all_probabilities: Record<string, number>;
  session_id: string;
  initial_message: string;
  face_detected: boolean;
  timestamp?: string;
}

export interface EmotionLog {
  id: string;
  session_id: string;
  emotion: string;
  confidence: number;
  face_detected: boolean;
  timestamp: string;
}

export interface EmotionStats {
  total_detections: number;
  emotion_counts: Record<string, number>;
}

/**
 * Detect emotion from image
 * Endpoint: POST /api/emotion/detect
 */
export const detectEmotion = async (
  imageData: string,
  sessionId?: string
): Promise<EmotionDetectionResponse> => {
  const response = await api.post<EmotionDetectionResponse>('/api/emotion/detect', {
    image: imageData,
    session_id: sessionId,
  });
  return response.data;
};

/**
 * Get emotion history for a session
 * Endpoint: GET /api/emotion/history/{session_id}
 */
export const getEmotionHistory = async (
  sessionId: string
): Promise<EmotionLog[]> => {
  const response = await api.get<EmotionLog[]>(`/api/emotion/history/${sessionId}`);
  return response.data;
};

/**
 * Get emotion stats
 * Endpoint: GET /api/emotion/stats
 */
export const getEmotionStats = async (): Promise<EmotionStats> => {
  const response = await api.get<EmotionStats>('/api/emotion/stats');
  return response.data;
};