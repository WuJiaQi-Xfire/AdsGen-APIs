
import { cn } from '@/lib/utils';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

interface PanelProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
  className?: string;
}

export const Panel = ({
  title,
  children,
  defaultOpen = true,
  className,
}: PanelProps) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className={cn("rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden", className)}>
      <div 
        className="flex items-center justify-between px-5 py-4 cursor-pointer"
        onClick={() => setIsOpen(!isOpen)}
      >
        <h3 className="font-medium text-sm">{title}</h3>
        <button type="button" className="p-1 rounded-full hover:bg-gray-100 transition-colors">
          {isOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </button>
      </div>
      
      {isOpen && (
        <div className="p-5 pt-0 border-t border-gray-100">
          {children}
        </div>
      )}
    </div>
  );
};
