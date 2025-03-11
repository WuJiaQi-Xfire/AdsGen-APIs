import React, { useState } from 'react';
import { Plus, Minus } from 'lucide-react';
import { cn } from '@/lib/utils';
import NumberInput from '@/components/NumberInput';
import Checkbox from '@/components/Checkbox';

//Could be refactored more, however layout&components not finalised, will see if can extract anything out later

interface ImageSetting {
  id: number;
  keywords: string;
  template: string;
  [key: string]: any;
}

interface ImageGenerationTabProps {
  ImageSetting: ImageSetting[];
  imageHeight: number;
  imageWidth: number;
  imagesPerPrompt: number;
  setImageHeight: (height: number) => void;
  setImageWidth: (width: number) => void;
  incrementImagesPerPrompt: () => void;
  decrementImagesPerPrompt: () => void;
}

//Might need more parameters for presets
export const ImageGenerationTab: React.FC<ImageGenerationTabProps> = ({
  ImageSetting,
  imageHeight,
  imageWidth,
  imagesPerPrompt,
  setImageHeight,
  setImageWidth,
  incrementImagesPerPrompt,
  decrementImagesPerPrompt,
}) => {
  const [selectedPrompts, setSelectedPrompts] = useState<number[]>([]);
  const [selectAll, setSelectAll] = useState(false);

  const togglePrompt = (id: number) => {
    if (selectedPrompts.includes(id)) {
      setSelectedPrompts(prev => prev.filter(promptId => promptId !== id));
      if (selectAll) setSelectAll(false);
    } else {
      setSelectedPrompts(prev => [...prev, id]);
      if (selectedPrompts.length + 1 === ImageSetting.length) {
        setSelectAll(true);
      }
    }
  };

  const toggleSelectAll = () => {
    if (selectAll) {
      setSelectedPrompts([]);
    } else {
      setSelectedPrompts(ImageSetting.map(prompt => prompt.id));
    }
    setSelectAll(!selectAll);
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <h2 className="text-xl font-semibold">Image Generation Settings</h2>
      <div className="grid grid-cols-3 gap-6">
        <NumberInput
          label="Image Height"
          value={imageHeight}
          onChange={setImageHeight}
          min={256}
          max={2048}
          step={1}
        />

        <NumberInput
          label="Image Width"
          value={imageWidth}
          onChange={setImageWidth}
          min={256}
          max={2048}
          step={1}
        />
        
        <div className="space-y-3">
          <label className="block text-sm font-medium text-gray-700">
            Images Per Prompt
          </label>
          <div className="flex items-center border border-gray-300 rounded-lg">
            <button
              onClick={decrementImagesPerPrompt}
              className="p-2 hover:bg-gray-100"
              disabled={imagesPerPrompt <= 1}
            >
              <Minus className="h-4 w-4" />
            </button>
            <div className="flex-1 text-center">{imagesPerPrompt}</div>
            <button
              onClick={incrementImagesPerPrompt}
              className="p-2 hover:bg-gray-100"
            >
              <Plus className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
      
      {ImageSetting.length > 0 && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-medium">Available Templates</h3>
            <button
              onClick={toggleSelectAll}
              className="text-sm text-brand-blue hover:underline"
            >
              {selectAll ? 'Deselect All' : 'Select All'}
            </button>
          </div>
          
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="w-12 px-4 py-3">
                    <div className="flex items-center justify-center">
                      <Checkbox checked={selectAll} onChange={toggleSelectAll} />
                    </div>
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Keywords
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Generated Template
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {ImageSetting.map((prompt) => (
                  <tr key={prompt.id} className="hover:bg-gray-50">
                    <td className="px-4 py-4">
                      <div className="flex items-center justify-center">
                      <Checkbox 
                        checked={selectedPrompts.includes(prompt.id)}  
                        onChange={() => togglePrompt(prompt.id)}
                        />
                      </div>
                    </td>
                    <td className="px-4 py-4 text-sm text-gray-900">
                      {prompt.keywords}
                    </td>
                    <td className="px-4 py-4 text-sm text-gray-500">
                      <div className="max-h-20 overflow-y-auto">
                        {prompt.template}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      <div className="pt-4">
        <button
          className={cn(
            "primary-button flex items-center",
            selectedPrompts.length === 0 ? "opacity-50 cursor-not-allowed" : ""
          )}
          disabled={selectedPrompts.length === 0}
          onClick={() => {
            if (selectedPrompts.length > 0) {
              // TODO: Send prompts to backend, need a properly crafted req after file handling is done
            }
          }}
        >
          Generate Images ({selectedPrompts.length*imagesPerPrompt})
        </button>
      </div>
    </div>
  );
};
