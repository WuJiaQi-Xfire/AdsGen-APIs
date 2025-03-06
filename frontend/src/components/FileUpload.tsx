
import { useState, useRef } from 'react';
import { Upload, X } from 'lucide-react';

interface FileUploadProps {
  label: string;
  onChange: (file: File | null) => void;
  accept?: string;
}

export const FileUpload = ({ 
  label, 
  onChange, 
  accept = ".csv" 
}: FileUploadProps) => {
  const [fileName, setFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    
    if (file) {
      setFileName(file.name);
      onChange(file);
    } else {
      setFileName(null);
      onChange(null);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleRemoveFile = () => { 
    setFileName(null);
    onChange(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = ''; 
    }
  };

  return (
    <div className="w-full">
      <label className="text-sm font-medium text-gray-700 mb-1.5 block">
        {label}
      </label>
      <div className="flex items-center">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept={accept}
          className="hidden"
        />
        {!fileName ? ( 
          <button
            type="button"
            onClick={handleButtonClick}
            className="flex items-center min-w-60 justify-center py-2 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors border border-gray-300" 
          >
            <Upload className="ml-2 mr-2 h-4 w-4" />
            Upload file
          </button>
        ) : (
          <div className="flex items-center bg-gray-100 border border-gray-200 rounded-xl p-2 max-w-xs"> 
            <span className="text-sm break-words">
              {fileName}
            </span>
            <button
              type="button"
              onClick={handleRemoveFile}
              className="ml-2 text-red-500 hover:text-red-700"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};