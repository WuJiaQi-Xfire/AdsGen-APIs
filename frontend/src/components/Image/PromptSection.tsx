import React from "react";
import { Upload, X } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { Textarea } from "@/components/UI/TextArea";

interface PromptSectionProps {
  hasPrompt: boolean;
  promptText: string;
  promptFileName: string;
  setPromptText: (text: string) => void;
  setHasPrompt: (hasPrompt: boolean) => void;
  handlePromptUpload: () => void;
  promptFileInputRef: React.RefObject<HTMLInputElement>;
  handlePromptFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const PromptSection: React.FC<PromptSectionProps> = ({
  hasPrompt,
  promptText,
  promptFileName,
  setPromptText,
  setHasPrompt,
  handlePromptUpload,
  promptFileInputRef,
  handlePromptFileUpload,
}) => {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">Prompt</label>
      {hasPrompt ? (
        <div className="border rounded-lg p-4 bg-background">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm font-medium">
              {promptFileName || "prompt.txt"}
            </p>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setHasPrompt(false)}
              className="h-8 w-8"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          <Textarea
            value={promptText}
            onChange={(e) => setPromptText(e.target.value)}
            className="min-h-32 transition-all-200"
          />
        </div>
      ) : (
        <div
          className="border-2 border-dashed rounded-lg p-4 text-center cursor-pointer hover:border-primary/50 hover:bg-accent transition-all-200"
          onClick={handlePromptUpload}
        >
          <div className="flex flex-col items-center justify-center py-2">
            <div className="bg-primary/10 rounded-full p-3 mb-2">
              <Upload className="h-5 w-5 text-primary" />
            </div>
            <p className="text-sm font-medium">Upload prompt file</p>
            <p className="text-xs text-muted-foreground mt-1">
              TXT or JSON (max. 1MB)
            </p>
          </div>

          <input
            ref={promptFileInputRef}
            type="file"
            className="hidden"
            accept=".txt,.json"
            onChange={handlePromptFileUpload}
          />
        </div>
      )}
    </div>
  );
};

export default PromptSection;
