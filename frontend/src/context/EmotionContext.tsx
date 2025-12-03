/**
 * Emotion Context - Manage emotion detection state
 */

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { v4 as uuidv4 } from 'uuid';
import {
  detectEmotion as apiDetectEmotion,
  EmotionDetectionResponse,
} from '../services/emotionApi';

interface EmotionContextType {
  sessionId: string;
  currentEmotion: EmotionDetectionResponse | null;
  emotionHistory: EmotionDetectionResponse[];
  detecting: boolean;
  detectEmotion: (imageData: string) => Promise<EmotionDetectionResponse>;
  resetSession: () => void;
}

const EmotionContext = createContext<EmotionContextType | undefined>(undefined);

export const EmotionProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // Generate or retrieve session ID
  const [sessionId] = useState<string>(() => {
    const stored = sessionStorage.getItem('emotion_session_id');
    if (stored) return stored;
    const newId = uuidv4();
    sessionStorage.setItem('emotion_session_id', newId);
    return newId;
  });

  const [currentEmotion, setCurrentEmotion] = useState<EmotionDetectionResponse | null>(null);
  const [emotionHistory, setEmotionHistory] = useState<EmotionDetectionResponse[]>([]);
  const [detecting, setDetecting] = useState(false);

  const detectEmotion = async (imageData: string): Promise<EmotionDetectionResponse> => {
    setDetecting(true);
    try {
      const result = await apiDetectEmotion(imageData, sessionId);
      setCurrentEmotion(result);
      setEmotionHistory(prev => [...prev, result]);
      return result;
    } catch (error) {
      console.error('Emotion detection failed:', error);
      throw error;
    } finally {
      setDetecting(false);
    }
  };

  const resetSession = () => {
    const newId = uuidv4();
    sessionStorage.setItem('emotion_session_id', newId);
    setCurrentEmotion(null);
    setEmotionHistory([]);
    window.location.reload();
  };

  return (
    <EmotionContext.Provider
      value={{
        sessionId,
        currentEmotion,
        emotionHistory,
        detecting,
        detectEmotion,
        resetSession,
      }}
    >
      {children}
    </EmotionContext.Provider>
  );
};

export const useEmotion = (): EmotionContextType => {
  const context = useContext(EmotionContext);
  if (!context) {
    throw new Error('useEmotion must be used within EmotionProvider');
  }
  return context;
};