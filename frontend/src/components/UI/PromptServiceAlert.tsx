import React, { useState, useEffect, useRef } from "react";
import { ApiService, HealthCheckResponse } from "@/lib/api";

interface PromptServiceAlertProps {
  triggerCheck?: boolean;
  onCheckComplete?: (isHealthy: boolean) => void;
}

const PromptServiceAlert: React.FC<PromptServiceAlertProps> = ({ 
  triggerCheck = false,
  onCheckComplete
}) => {
  const [healthStatus, setHealthStatus] = useState<HealthCheckResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [visible, setVisible] = useState<boolean>(false);
  const [countdown, setCountdown] = useState<number>(30);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const [shouldCheckAgain, setShouldCheckAgain] = useState<boolean>(true);

  const checkHealth = async () => {
    setLoading(true);
    try {
      const response = await ApiService.checkHealth();
      setHealthStatus(response);
      
      // Only check GPT service for prompt generation
      const isGptHealthy = response.gpt.status === "healthy";
      setVisible(!isGptHealthy);
      
      // If service is healthy, we don't need to check again
      setShouldCheckAgain(!isGptHealthy);
      
      if (onCheckComplete) {
        onCheckComplete(isGptHealthy);
      }
    } catch (error) {
      console.error("Failed to check service health:", error);
      setVisible(true);
      setShouldCheckAgain(true);
      if (onCheckComplete) {
        onCheckComplete(false);
      }
    } finally {
      setLoading(false);
    }
  };

  // Countdown timer
  useEffect(() => {
    // Clear any existing timer
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    
    // Only start the timer if we need to check again
    if (shouldCheckAgain) {
      timerRef.current = setInterval(() => {
        setCountdown(prev => {
          if (prev <= 0) {
            checkHealth();
            return 30;
          }
          return prev - 1;
        });
      }, 1000);
    }
    
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [shouldCheckAgain]);
  
  // Check health on mount
  useEffect(() => {
    // Check immediately when component mounts
    checkHealth();
  }, []);

  // Check health when triggerCheck changes to true
  useEffect(() => {
    if (triggerCheck) {
      checkHealth();
    }
  }, [triggerCheck]);

  if (!visible || !healthStatus) return null;

  return (
    <div className="w-full bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3">
          <p className="text-sm text-yellow-700">
            <span className="font-medium">ChatGPT Service Issue:</span> {healthStatus.gpt.message}
          </p>
          <p className="mt-1 text-xs text-yellow-700">
            Prompt generation may not work correctly. System will automatically check again in <span className="font-medium">{countdown}</span> seconds.
          </p>
        </div>
      </div>
      {loading && (
        <div className="mt-2 flex items-center">
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-yellow-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="text-xs text-yellow-700">Checking service status...</span>
        </div>
      )}
    </div>
  );
};

export default PromptServiceAlert;
