
import { useState, KeyboardEvent } from 'react';
import { X } from 'lucide-react';

interface TagInputProps {
  tags: string[];
  onChange: (tags: string[]) => void;
  placeholder?: string;
  label?: string;
}

export const TagInput = ({
  tags,
  onChange,
  placeholder = "Type to add...",
  label
}: TagInputProps) => {
  const [input, setInput] = useState('');

  const addTag = (tag: string) => {
    const trimmedTag = tag.trim();
    if (trimmedTag && !tags.includes(trimmedTag)) {
      const newTags = [...tags, trimmedTag];
      onChange(newTags);
    }
    setInput('');
  };

  const removeTag = (indexToRemove: number) => {
    const newTags = tags.filter((_, index) => index !== indexToRemove);
    onChange(newTags);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addTag(input);
    }
  };

  return (
    <div className="w-full">
      {label && (
        <label className="text-sm font-medium text-gray-700 mb-1.5 block">
          {label}
        </label>
      )}
      
      <div className="input-field flex flex-wrap gap-2 min-h-[46px] bg-white">
        {tags.map((tag, index) => (
          <div 
            key={index} 
            className="flex items-center bg-gray-100 rounded-full px-3 py-1 text-sm"
          >
            <span className="mr-1">{tag}</span>
            <button
              type="button"
              onClick={() => removeTag(index)}
              className="text-gray-500 hover:text-gray-700"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        ))}
        
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => input && addTag(input)}
          placeholder={tags.length === 0 ? placeholder : ''}
          className="flex-grow outline-none bg-transparent text-sm min-w-[120px]"
        />
      </div>
      
      <p className="text-xs text-gray-500 mt-2">
        Press Enter or comma to add
      </p>
    </div>
  );
};
