import React from "react";
import { Upload } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { Label } from "@/components/UI/Label";
import { Checkbox } from "@/components/UI/Checkbox";

interface PromptFile {
  id: string;
  name: string;
  selected: boolean;
}

interface PromptSectionProps {
  hasPrompt: boolean;
  promptFiles: PromptFile[];
  handlePromptUpload: () => void;
  togglePromptSelection: (id: string) => void;
  promptFileInputRef: React.RefObject<HTMLInputElement>;
  handlePromptFileUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const PromptSection: React.FC<PromptSectionProps> = ({
  hasPrompt,
  promptFiles,
  handlePromptUpload,
  togglePromptSelection,
  promptFileInputRef,
  handlePromptFileUpload,
}) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium">Prompts</label>
        <input
          ref={promptFileInputRef}
          type="file"
          className="hidden"
          accept=".txt"
          multiple
          onChange={handlePromptFileUpload}
        />
        <Button
          variant="ghost"
          size="sm"
          onClick={() => promptFileInputRef.current?.click()}
          className="h-8 text-xs"
        >
          Upload more
        </Button>
      </div>

      {hasPrompt ? (
        <div className="border rounded-lg p-4 bg-background">
          <div className="max-h-64 overflow-y-auto">
            <div className="grid grid-cols-2 gap-2">
              {promptFiles.map((file) => (
                <div
                  key={file.id}
                  className="flex items-center gap-2 p-2 bg-muted/40 rounded-md"
                >
                  <Checkbox
                    id={`prompt-${file.id}`}
                    checked={file.selected}
                    onCheckedChange={() => togglePromptSelection(file.id)}
                  />
                  <Label
                    htmlFor={`prompt-${file.id}`}
                    className="flex-1 font-medium truncate text-sm"
                  >
                    {file.name}
                  </Label>
                </div>
              ))}
            </div>
          </div>
          {promptFiles.length === 0 && (
            <div className="text-center py-4 text-muted-foreground">
              No prompt files. Upload some to get started.
            </div>
          )}
        </div>
      ) : (
        <div
          className="border-2 border-dashed rounded-lg p-4 text-center cursor-pointer hover:border-primary/50 hover:bg-accent transition-all-200"
          onClick={() => promptFileInputRef.current?.click()}
        >
          <div className="flex flex-col items-center justify-center py-2">
            <div className="bg-primary/10 rounded-full p-3 mb-2">
              <Upload className="h-5 w-5 text-primary" />
            </div>
            <p className="text-sm font-medium">Upload prompt files</p>
            <p className="text-xs text-muted-foreground mt-1">
              One or more TXT files
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PromptSection;
