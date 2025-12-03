import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card";

interface ChatBubbleProps {
  message: string;
  isUser: boolean;
  // ✅ FIX: Definisikan timestamp sebagai string agar cocok dengan Detect.tsx
  timestamp?: string; 
  isEmergency?: boolean;
  hotlines?: any;
}

const ChatBubble = ({ 
  message, 
  isUser, 
  timestamp, 
  isEmergency, 
  hotlines 
}: ChatBubbleProps) => {
  return (
    <div className={cn(
      "flex w-full mt-2 space-x-3 max-w-xs md:max-w-md",
      isUser ? "ml-auto justify-end" : ""
    )}>
      <div className={cn("flex flex-col", isUser ? "items-end" : "items-start")}>
        <div className={cn(
          "px-4 py-2 rounded-lg shadow-sm text-sm relative",
          isUser 
            ? "bg-blue-600 text-white rounded-br-none" 
            : isEmergency 
              ? "bg-red-100 text-red-900 border border-red-200 rounded-bl-none"
              : "bg-white border border-gray-200 text-gray-800 rounded-bl-none"
        )}>
          {/* Tampilkan Pesan */}
          <p className="whitespace-pre-wrap leading-relaxed">{message}</p>
          
          {/* Tampilkan Hotline jika Emergency */}
          {isEmergency && hotlines && (
            <div className="mt-3 pt-2 border-t border-red-200">
              <p className="font-bold text-xs mb-1">⚠️ Bantuan Darurat:</p>
              <ul className="text-xs space-y-1">
                {hotlines.map((h: any, idx: number) => (
                  <li key={idx} className="flex justify-between">
                    <span>{h.name}:</span>
                    <a href={`tel:${h.number}`} className="font-bold hover:underline">
                      {h.number}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
        
        {/* Tampilkan Timestamp */}
        {timestamp && (
          <span className="text-[10px] text-gray-400 mt-1 px-1">
            {timestamp}
          </span>
        )}
      </div>
    </div>
  );
};

export default ChatBubble;