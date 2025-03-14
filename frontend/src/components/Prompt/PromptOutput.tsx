import React from "react";
import { Textarea } from "@/components/UI/TextArea";
import { Button } from "@/components/UI/PrimaryButton";

interface PromptOutputProps {
  generatedPrompt: string;
}

const PromptOutput: React.FC<PromptOutputProps> = ({ generatedPrompt }) => {

  const downloadAsTxtFile = () => {
    const blob = new Blob([generatedPrompt], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "generated-prompt.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  
  return (
    <div className="space-y-2 mt-6 animate-fade-in">
      <label className="text-sm font-medium">Generated Prompt</label>
      <div className="border rounded-lg p-4 bg-background">
        <Textarea
          value={generatedPrompt}
          readOnly
          className="min-h-32 bg-background"
        />
        <div className="flex justify-end mt-2">
        <Button 
            variant="outline" 
            size="sm" 
            onClick={downloadAsTxtFile}
          >
            Download as .txt
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={() => navigator.clipboard.writeText(generatedPrompt)}
          >
            Copy to Clipboard
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PromptOutput;
