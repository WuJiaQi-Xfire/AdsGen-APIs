
import { cn } from '@/lib/utils';

interface ModelOption {
  id: string;
  name: string;
}

interface ModelSelectorProps {
  options: ModelOption[];
  defaultSelected?: string;
  onChange: (id: string) => void;
}

export const ModelSelector = ({ 
  options, 
  defaultSelected = options[0]?.id, 
  onChange 
}: ModelSelectorProps) => {
  const handleSelect = (id: string) => {
    onChange(id);
  };

  return (
    <div className="w-full animate-fade-in">
      <div className="flex flex-col space-y-3">
        <p className="text-sm font-medium text-gray-700">AI Model</p>
        
        <div className="flex flex-col space-y-2">
          {options.map((option) => (
            <label 
              key={option.id}
              className={cn(
                "flex items-center p-3 rounded-lg border cursor-pointer transition-all",
                defaultSelected === option.id 
                  ? "border-brand-blue bg-blue-50" 
                  : "border-gray-200 hover:bg-gray-50"
              )}
            >
              <div 
                className={cn(
                  "flex items-center justify-center w-5 h-5 rounded-full border mr-3 relative",
                  defaultSelected === option.id 
                    ? "border-brand-blue" 
                    : "border-gray-300"
                )}
              >
                <input
                  type="radio"
                  className="sr-only"
                  name="model-selection"
                  value={option.id}
                  checked={defaultSelected === option.id}
                  onChange={() => handleSelect(option.id)}
                />
                {defaultSelected === option.id && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-2.5 h-2.5 rounded-full bg-brand-blue" />
                  </div>
                )}
              </div>
              <span className="text-sm">{option.name}</span>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};
