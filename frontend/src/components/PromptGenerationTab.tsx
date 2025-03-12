import React, { useState } from "react";
import { Button } from "@/components/PrimaryButton";
import { Textarea } from "@/components/TextArea";
import { Upload, ArrowRight, Check } from "lucide-react";
import { toast } from "@/components/ToastManager";

const PromptGeneration: React.FC = () => {
  const [description, setDescription] = useState(
    "Example: 50/50 split image, depicting the evil and good side of a place"
  );
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedPrompt, setGeneratedPrompt] = useState("");
  const [hasReferenceImage, setHasReferenceImage] = useState(false);
  const [fileName, setFileName] = useState("");

  const handleGenerate = () => {
    setIsGenerating(true);
    // Text as placeholder for now, TODO Call GPT to generate prompt
    setTimeout(() => {
      setIsGenerating(false);
      setGeneratedPrompt(
        "You are an AI artist specializing in dynamic split-screen advertisements. " +
          "Generate a detailed image description using:  " +
          "- **Art Style**: [Use verbatim from {art_style_list}]" +
          "- **Theme**: {Keywords}  - **Structure**: Central region (75%), vertical sidebar (25%)." +
          "- **Intent**: Contrast 'problem state' (central) with 'solution state' (sidebar)."
      );
      toast.show({
        id: "my-id",
        icon: <Check className="h-4 w-4" />,
        message: "Your ad template prompt has been generated successfully.",
        duration: 1500,
      });
    }, 2000);
  };

  const handleReferenceImageUpload = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    // TODO: file handling for image upload
    if (e.target.files && e.target.files.length > 0) {
      setHasReferenceImage(true);
      setFileName(e.target.files[0].name);
      toast.show({
        id: "my-id",
        icon: <Check className="h-4 w-4" />,
        message: "Your reference image will be used in the prompt generation.",
        duration: 1500,
      });
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-1">
          Ad Template Prompt Generation
        </h1>
        <p className="text-muted-foreground">
          Create detailed prompts for your ad templates
        </p>
      </div>

      <div className="space-y-6">
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

        <div className="space-y-2">
          <label className="text-sm font-medium">Upload reference image</label>
          <label
            className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer hover:border-primary/50 hover:bg-accent transition-all-200 block ${
              hasReferenceImage ? "border-primary/50 bg-primary/5" : ""
            }`}
          >
            <input
              type="file"
              className="hidden"
              accept="image/*"
              onChange={handleReferenceImageUpload}
            />
            <div className="flex flex-col items-center justify-center py-4">
              <div className="bg-primary/10 rounded-full p-3 mb-2">
                {hasReferenceImage ? (
                  <Check className="h-6 w-6 text-primary" />
                ) : (
                  <Upload className="h-6 w-6 text-primary" />
                )}
              </div>
              <p className="text-sm font-medium">
                {hasReferenceImage ? fileName : "Click to upload image"}
              </p>
              {/* Supported image types by Vision */}
              <p className="text-xs text-muted-foreground mt-1">
                PNG, JPEG, Webp, GIF
              </p>
            </div>
          </label>
        </div>

        <Button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="w-full"
          size="lg"
        >
          {isGenerating ? (
            "Generating..."
          ) : (
            <>
              Generate Prompt <ArrowRight className="ml-2 h-4 w-4" />
            </>
          )}
        </Button>

        {generatedPrompt && (
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
                  onClick={() => navigator.clipboard.writeText(generatedPrompt)}
                >
                  Copy to Clipboard
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PromptGeneration;
