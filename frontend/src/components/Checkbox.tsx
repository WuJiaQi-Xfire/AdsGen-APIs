import React from 'react';
import { Check } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CheckboxProps {
  checked: boolean;
  onChange: () => void;
}

const Checkbox: React.FC<CheckboxProps> = ({ checked, onChange }) => {
  return (
    <div
      className={cn(
        "h-5 w-5 rounded border flex items-center justify-center cursor-pointer",
        checked ? "bg-brand-blue border-brand-blue" : "border-gray-300"
      )}
      onClick={onChange}
    >
      {checked && <Check className="h-3 w-3 text-white" />}
    </div>
  );
};

export default Checkbox;
