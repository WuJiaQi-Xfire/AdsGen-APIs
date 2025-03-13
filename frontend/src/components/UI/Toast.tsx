import { cn } from "@/lib/utils";
import { useEffect } from "react";

export interface ToastProps {
  id: string;
  destroy: () => void;
  message: string;
  duration?: number;
}

const Toast: React.FC<ToastProps> = (props) => {
  const { destroy, message, duration = 0} = props;

  useEffect(() => {
    if (!duration) return;

    const timer = setTimeout(() => {
      destroy();
    }, duration);

    return () => clearTimeout(timer);
  }, [destroy, duration]);

  return (
    <div
      className={cn(
        "flex items-center bg-gray-100 border border-gray-300 rounded py-2 px-4 mb-4"
      )}
    >
      <span className="text-xs pl-2">{message}</span>
    </div>
  );
};

export default Toast;
