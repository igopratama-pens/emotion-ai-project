/**
 * ============================================================================
 * FIXED: ChatContext.tsx
 * ============================================================================
 */

import React, { createContext, useContext, useState, ReactNode } from 'react';
import {
  sendChatMessage as apiSendMessage,
  ChatRequest,
  ChatResponse,
} from '../services/chatApi';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  isEmergency?: boolean;
  hotlines?: string[];
}

interface ChatContextType {
  messages: Message[];
  sending: boolean;
  sendMessage: (
    message: string,
    emotion: string,
    sessionId: string,
    emotionLogId?: string
  ) => Promise<void>;
  // ✅ FIXED: Added addAiMessage to interface
  addAiMessage: (message: string) => void;
  clearChat: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sending, setSending] = useState(false);

  // ✅ FIXED: Implement addAiMessage function
  const addAiMessage = (message: string) => {
    const aiMessage: Message = {
      id: Date.now().toString(),
      content: message,
      isUser: false,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, aiMessage]);
  };

  const sendMessage = async (
    message: string,
    emotion: string,
    sessionId: string,
    emotionLogId?: string
  ) => {
    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      content: message,
      isUser: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);

    setSending(true);
    try {
      // Build history for context
      const history = messages.map((msg) => ({
        role: msg.isUser ? 'user' : 'assistant',
        content: msg.content,
      }));

      // ✅ FIXED: Prepare request with required fields
      const request: ChatRequest = {
        emotion,
        message,
        session_id: sessionId,
        emotion_log_id: emotionLogId || '', // Ensure string
        history,
      };

      const response: ChatResponse = await apiSendMessage(request);

      // Add AI response
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        isUser: false,
        timestamp: new Date(),
        isEmergency: response.emergency,
        hotlines: response.hotlines,
      };
      setMessages((prev) => [...prev, aiResponse]);
    } catch (error) {
      console.error('Failed to send message:', error);

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Maaf, terjadi kesalahan. Silakan coba lagi.',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setSending(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        sending,
        sendMessage,
        addAiMessage, // ✅ Expose the function
        clearChat,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within ChatProvider');
  }
  return context;
};