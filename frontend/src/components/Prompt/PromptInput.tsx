import React from "react";
import { Textarea } from "@/components/UI/TextArea";

interface PromptInputProps {
  description: string;
  setDescription: (description: string) => void;
}

const PromptInput: React.FC<PromptInputProps> = ({
  description,
  setDescription,
}) => {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">
        Describe the image you want to generate:
      </label>
      <Textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Example: side by side, 50%"
        className="min-h-24"
      />
    </div>
  );
};

export default PromptInput;
