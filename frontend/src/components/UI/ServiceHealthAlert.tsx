import React, { useState, useEffect } from "react";
import { ApiService, HealthCheckResponse } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ServiceHealthAlertProps {
  onClose?: () => void;
}

// Use localStorage to track if the alert has been shown and closed
const ALERT_CLOSED_KEY = 'service-health-alert-closed';

const ServiceHealthAlert: React.FC<ServiceHealthAlertProps> = ({ onClose }) => {
  const [healthStatus, setHealthStatus] = useState<HealthCheckResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [visible, setVisible] = useState<boolean>(false);
  
  // Check if the alert has been closed before
  const [alertClosedBefore, setAlertClosedBefore] = useState<boolean>(() => {
    return localStorage.getItem(ALERT_CLOSED_KEY) === 'true';
  });

  const checkHealth = async () => {
    setLoading(true);
    try {
      const response = await ApiService.checkHealth();
      setHealthStatus(response);
      // Only show the alert if it hasn't been closed before
      setVisible(!response.all_healthy && !alertClosedBefore);
    } catch (error) {
      console.error("Failed to check service health:", error);
      setVisible(!alertClosedBefore);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, [alertClosedBefore]);

  const handleRefresh = () => {
    checkHealth();
  };

  const handleClose = () => {
    setVisible(false);
    // Remember that the alert has been closed
    localStorage.setItem(ALERT_CLOSED_KEY, 'true');
    setAlertClosedBefore(true);
    if (onClose) onClose();
  };

  if (!visible || !healthStatus) return null;

  const unhealthyServices = [
    { name: "Database", status: healthStatus.database.status, message: healthStatus.database.message },
    { name: "ComfyUI", status: healthStatus.comfyui.status, message: healthStatus.comfyui.message },
    { name: "GPT API", status: healthStatus.gpt.status, message: healthStatus.gpt.message },
    { name: "Frontend-Backend", status: healthStatus.frontend_backend.status, message: healthStatus.frontend_backend.message },
  ].filter(service => service.status === "unhealthy");

  return (
    <div className="fixed top-4 left-0 right-0 mx-auto z-50 max-w-2xl bg-white rounded-lg shadow-lg border border-red-300 p-6">
      <div className="flex justify-between items-start">
        <div className="flex items-center">
          <div className="flex-shrink-0 text-red-500">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-base font-medium text-gray-900">Service Health Alert</h3>
            <div className="mt-1 text-sm text-gray-500">
              <p>Some services are not available:</p>
              <ul className="list-disc pl-5 mt-2 space-y-2">
                {unhealthyServices.map((service, index) => (
                  <li key={index} className="text-sm">
                    <span className="font-medium">{service.name}:</span> {service.message}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        <button
          type="button"
          className="ml-4 text-gray-400 hover:text-gray-500 focus:outline-none"
          onClick={handleClose}
        >
          <span className="sr-only">Close</span>
          <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
      <div className="mt-4 flex">
        <button
          type="button"
          className={cn(
            "inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
            loading && "opacity-50 cursor-not-allowed"
          )}
          onClick={handleRefresh}
          disabled={loading}
        >
          {loading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Checking...
            </>
          ) : (
            <>
              <svg className="-ml-1 mr-2 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh Services
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ServiceHealthAlert;
