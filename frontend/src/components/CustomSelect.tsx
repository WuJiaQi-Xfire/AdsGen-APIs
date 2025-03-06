
import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SelectOption {
  value: string;
  label: string;
}

interface CustomSelectProps {
  options: SelectOption[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  className?: string;
}

export const CustomSelect = ({
  options,
  value,
  onChange,
  placeholder = "Select an option",
  label,
  className
}: CustomSelectProps) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const selectedOption = options.find(option => option.value === value);
  
  return (
    <div className={cn("relative", className)}>
      {label && (
        <label className="text-sm font-medium text-gray-700 mb-1.5 block">
          {label}
        </label>
      )}
      
      <div className="relative">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="select-field w-full flex items-center justify-between"
        >
          <span className={cn("block truncate", !selectedOption && "text-gray-400")}>
            {selectedOption ? selectedOption.label : placeholder}
          </span>
          {isOpen ? (
            <ChevronUp className="h-4 w-4 text-gray-500" />
          ) : (
            <ChevronDown className="h-4 w-4 text-gray-500" />
          )}
        </button>
        
        {isOpen && (
          <div className="absolute z-10 mt-1 w-full rounded-lg border border-gray-200 bg-white py-1 shadow-lg animate-fade-in">
            {options.map((option) => (
              <div
                key={option.value}
                className={cn(
                  "cursor-pointer px-4 py-2.5 text-sm hover:bg-gray-50",
                  value === option.value && "bg-gray-50 text-brand-blue"
                )}
                onClick={() => {
                  onChange(option.value);
                  setIsOpen(false);
                }}
              >
                {option.label}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
