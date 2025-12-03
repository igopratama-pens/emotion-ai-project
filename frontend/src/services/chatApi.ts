/**
 * ============================================================================
 * FIXED: chatApi.ts
 * ============================================================================
 */

import api from './api';

export interface ChatMessage {
  id?: string;
  session_id: string;
  emotion_log_id?: string;
  message: string;
  response: string;
  is_user: boolean;
  is_crisis?: boolean;
  timestamp?: string;
}

export interface ChatRequest {
  emotion: string;
  message: string;
  session_id: string;
  emotion_log_id: string; // ✅ FIXED: Changed to REQUIRED (not optional)
  history?: Array<{ role: string; content: string }>;
}

export interface ChatResponse {
  response: string;
  emergency?: boolean;
  hotlines?: string[];
  message_id?: string;
}

/**
 * Send message to chatbot
 */
export const sendChatMessage = async (
  request: ChatRequest
): Promise<ChatResponse> => {
  // ✅ FIXED: Ensure emotion_log_id is sent (use empty string if undefined)
  const payload = {
    ...request,
    emotion_log_id: request.emotion_log_id || '',
    history: request.history || [],
  };

  const response = await api.post<ChatResponse>('/api/chat/', payload);
  return response.data;
};

/**
 * Get chat history for a session
 */
export const getChatHistory = async (
  sessionId: string
): Promise<ChatMessage[]> => {
  const response = await api.get<ChatMessage[]>(`/api/chat/history/${sessionId}`);
  return response.data;
};

/**
 * Get all chat logs (admin only)
 */
export const getAllChatLogs = async (
  limit = 100,
  offset = 0
): Promise<{ logs: ChatMessage[]; total: number }> => {
  const response = await api.get('/api/chat/logs', {
    params: { limit, offset },
  });
  return response.data;
};