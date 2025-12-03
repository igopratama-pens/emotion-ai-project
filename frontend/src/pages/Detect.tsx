import { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { useToast } from '@/hooks/use-toast';
import { Camera, RefreshCw, Send, Music, UtensilsCrossed, Activity } from 'lucide-react';
import ChatBubble from '@/components/ChatBubble';
import { useEmotion } from '@/context/EmotionContext';
import { useChat } from '@/context/ChatContext';
import { getRecommendations, trackRecommendationClick, Recommendation } from '@/services/recommendationApi';

const EMOTION_COLORS: Record<string, string> = {
  Happiness: 'bg-yellow-500',
  Sadness: 'bg-blue-500',
  Anger: 'bg-red-500',
  Fear: 'bg-purple-500',
  Surprise: 'bg-orange-500',
  Disgust: 'bg-green-500',
  Neutral: 'bg-gray-500',
};

export default function Detect() {
  const webcamRef = useRef<Webcam>(null);
  const { toast } = useToast();
  
  // Context
  const { sessionId, currentEmotion, detecting, detectEmotion, resetSession } = useEmotion();
  const { messages, sending, sendMessage, addAiMessage, clearChat } = useChat();
  
  // Local state
  const [capturing, setCapturing] = useState(false);
  const [countdown, setCountdown] = useState<number | null>(null);
  const [chatInput, setChatInput] = useState('');
  const [recommendations, setRecommendations] = useState<{
    music: Recommendation[];
    food: Recommendation[];
    activity: Recommendation[];
  } | null>(null);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);

  // Load recommendations when emotion detected
  useEffect(() => {
    if (currentEmotion?.emotion) {
      loadRecommendations(currentEmotion.emotion);
    }
  }, [currentEmotion]);

  const loadRecommendations = async (emotion: string) => {
    setLoadingRecommendations(true);
    try {
      const data = await getRecommendations(emotion);
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    } finally {
      setLoadingRecommendations(false);
    }
  };

  const handleCapture = useCallback(() => {
    setCapturing(true);
    setCountdown(3);

    const countdownInterval = setInterval(() => {
      setCountdown((prev) => {
        if (prev === 1) {
          clearInterval(countdownInterval);
          captureImage();
          return null;
        }
        return prev ? prev - 1 : null;
      });
    }, 1000);
  }, [sessionId]);

  const captureImage = async () => {
    if (!webcamRef.current) return;

    try {
      // ✅ FIX: Hapus parameter resize ({width: 500...}).
      // Gunakan default (kosong) agar mengambil resolusi ASLI webcam (Full Quality).
      // Ini penting agar MediaPipe bisa mendeteksi detail wajah dengan akurat.
      const imageSrc = webcamRef.current.getScreenshot();
      
      if (!imageSrc) {
        throw new Error('Failed to capture image');
      }

      // Call API
      const result = await detectEmotion(imageSrc); 

      toast({
        title: 'Deteksi Berhasil!',
        description: `Emosi: ${result.emotion} (${(result.confidence * 100).toFixed(1)}%)`,
      });

      // Display AI greeting using addAiMessage
      if (result.initial_message) {
        addAiMessage(result.initial_message);
      }

    } catch (error: any) {
      console.error('Detection failed:', error);
      toast({
        title: 'Deteksi Gagal',
        description: error.response?.data?.detail || 'Gagal memproses gambar.',
        variant: 'destructive',
      });
    } finally {
      setCapturing(false);
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !currentEmotion) return;

    const message = chatInput.trim();
    setChatInput('');

    // Send user message to backend
    await sendMessage(message, currentEmotion.emotion, sessionId);
  };

  const handleRecommendationClick = async (
    type: 'music' | 'food' | 'activity',
    recommendation: Recommendation
  ) => {
    // 1. Open link immediately (UX priority)
    if (recommendation.link) {
      window.open(recommendation.link, '_blank');
    }

    if (!currentEmotion) return;

    // 2. Track click in background
    try {
      await trackRecommendationClick({
        session_id: sessionId,
        emotion_log_id: undefined, // Let backend handle
        emotion: currentEmotion.emotion,
        category: type,
        title: recommendation.title,
      });
    } catch (error) {
      console.error('Tracking failed (link still opened):', error);
    }
  };

  const handleReset = () => {
    resetSession();
    clearChat();
    setRecommendations(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Deteksi Emosi
          </h1>
          <p className="text-gray-600">
            Tangkap wajahmu dan chat dengan AI tentang perasaanmu
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Left Column: Camera + Emotion Result */}
          <div className="space-y-6">
            <Card className="p-6">
              <div className="relative aspect-video bg-black rounded-lg overflow-hidden mb-4">
                <Webcam
                  ref={webcamRef}
                  audio={false}
                  screenshotFormat="image/jpeg"
                  className="w-full h-full object-cover"
                  mirrored
                />
                {countdown !== null && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black/50">
                    <div className="text-white text-8xl font-bold animate-pulse">
                      {countdown}
                    </div>
                  </div>
                )}
              </div>

              <div className="flex gap-3">
                <Button
                  onClick={handleCapture}
                  disabled={capturing || detecting}
                  className="flex-1"
                  size="lg"
                >
                  <Camera className="mr-2 h-5 w-5" />
                  {capturing ? 'Menangkap...' : detecting ? 'Mendeteksi...' : 'Tangkap Foto'}
                </Button>
                <Button
                  onClick={handleReset}
                  variant="outline"
                  size="lg"
                >
                  <RefreshCw className="h-5 w-5" />
                </Button>
              </div>
            </Card>

            {currentEmotion && (
              <Card className="p-6">
                <h3 className="text-xl font-semibold mb-4">Hasil Deteksi</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Emosi:</span>
                    <Badge
                      className={`${EMOTION_COLORS[currentEmotion.emotion] || 'bg-gray-500'} text-white text-lg px-4 py-2`}
                    >
                      {currentEmotion.emotion}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Confidence:</span>
                    <span className="text-lg font-semibold">
                      {(currentEmotion.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Wajah Terdeteksi:</span>
                    <Badge variant={currentEmotion.face_detected ? 'default' : 'secondary'}>
                      {currentEmotion.face_detected ? 'Ya' : 'Tidak'}
                    </Badge>
                  </div>
                </div>
              </Card>
            )}
          </div>

          {/* Right Column: Chat */}
          <Card className="p-6 flex flex-col h-[600px]">
            <h3 className="text-xl font-semibold mb-4">Chat dengan AI</h3>
            
            {!currentEmotion ? (
              <div className="flex-1 flex items-center justify-center text-gray-400">
                <p>Tangkap foto wajahmu untuk mulai chat</p>
              </div>
            ) : (
              <>
                <div className="flex-1 overflow-y-auto space-y-3 mb-4 p-2 scrollbar-thin">
                  {messages.map((msg, idx) => (
                    <ChatBubble
                      key={idx}
                      message={msg.content}
                      isUser={msg.isUser}
                      // Pastikan timestamp ada sebelum format
                      timestamp={msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : undefined}
                      isEmergency={msg.isEmergency}
                      hotlines={msg.hotlines}
                    />
                  ))}
                  {sending && (
                    <div className="text-center text-gray-400 text-sm mt-2">
                      <span className="animate-pulse">AI sedang mengetik...</span>
                    </div>
                  )}
                </div>

                <div className="flex gap-2 mt-auto">
                  <Input
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Ceritakan perasaanmu..."
                    disabled={sending}
                    className="flex-1"
                  />
                  <Button
                    onClick={handleSendMessage}
                    disabled={sending || !chatInput.trim()}
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </>
            )}
          </Card>
        </div>

        {/* Recommendations Section */}
        {currentEmotion && recommendations && (
          <div className="mt-8 mb-12">
            <Card className="p-6">
              <h3 className="text-2xl font-bold mb-6">Rekomendasi untuk {currentEmotion.emotion}</h3>
              
              {loadingRecommendations ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto mb-2"></div>
                  <span className="text-gray-400">Memuat rekomendasi...</span>
                </div>
              ) : (
                <div className="space-y-8">
                  {/* Music */}
                  <div>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="p-2 bg-purple-100 rounded-lg">
                        <Music className="h-5 w-5 text-purple-600" />
                      </div>
                      <h4 className="text-lg font-semibold">Musik</h4>
                    </div>
                    <div className="grid md:grid-cols-3 gap-4">
                      {recommendations.music.map((item, idx) => (
                        <Card
                          key={idx}
                          className="p-4 cursor-pointer hover:shadow-lg transition hover:border-purple-200 group"
                          onClick={() => handleRecommendationClick('music', item)}
                        >
                          <h5 className="font-semibold mb-2 group-hover:text-purple-600 transition">{item.title}</h5>
                          <p className="text-sm text-gray-600">{item.description}</p>
                        </Card>
                      ))}
                    </div>
                  </div>

                  <Separator />

                  {/* Food */}
                  <div>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="p-2 bg-orange-100 rounded-lg">
                        <UtensilsCrossed className="h-5 w-5 text-orange-600" />
                      </div>
                      <h4 className="text-lg font-semibold">Makanan</h4>
                    </div>
                    <div className="grid md:grid-cols-3 gap-4">
                      {recommendations.food.map((item, idx) => (
                        <Card
                          key={idx}
                          className="p-4 cursor-pointer hover:shadow-lg transition hover:border-orange-200 group"
                          onClick={() => handleRecommendationClick('food', item)}
                        >
                          <h5 className="font-semibold mb-2 group-hover:text-orange-600 transition">{item.title}</h5>
                          <p className="text-sm text-gray-600">{item.description}</p>
                        </Card>
                      ))}
                    </div>
                  </div>

                  <Separator />

                  {/* Activities */}
                  <div>
                    <div className="flex items-center gap-2 mb-4">
                      <div className="p-2 bg-green-100 rounded-lg">
                        <Activity className="h-5 w-5 text-green-600" />
                      </div>
                      <h4 className="text-lg font-semibold">Aktivitas</h4>
                    </div>
                    <div className="grid md:grid-cols-3 gap-4">
                      {recommendations.activity.map((item, idx) => (
                        <Card 
                          key={idx} 
                          className="p-4 cursor-pointer hover:shadow-lg transition hover:border-green-200 group"
                          onClick={() => handleRecommendationClick('activity', item)}
                        >
                          <h5 className="font-semibold mb-2 group-hover:text-green-600 transition">{item.title}</h5>
                          <p className="text-sm text-gray-600">{item.description}</p>
                        </Card>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}