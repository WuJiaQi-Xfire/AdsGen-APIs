import React from "react";
import { Button } from "@/components/UI/PrimaryButton";
import { ArrowRight } from "lucide-react";
import PromptInput from "./Prompt/PromptInput";
import ReferenceImage from "./Prompt/ReferenceImage";
import PromptOutput from "./Prompt/PromptOutput";
import { PromptGeneration } from "@/lib/PromptGeneration";
import { showToast } from "@/lib/ShowToast";

const PromptGenerationTab: React.FC = () => {
  const {
    description,
    setDescription,
    isGenerating,
    generatedPrompt,
    hasReferenceImage,
    fileName,
    imageUrl,
    setImageUrl,
    handleGenerate,
    handleReferenceImageUpload,
    clearReferenceImage,
  } = PromptGeneration();

  const validateAndGenerate = () => {
    if (!description.trim()) {
      showToast("Please enter a description for your image.");
      return;
    }
    handleGenerate();
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
        <div className="bg-white rounded-lg shadow-soft p-5 border">
          <PromptInput
            description={description}
            setDescription={setDescription}
          />
        </div>

        <div className="bg-white rounded-lg shadow-soft p-5 border">
          <ReferenceImage
            hasReferenceImage={hasReferenceImage}
            fileName={fileName}
            imageUrl={imageUrl}
            setImageUrl={setImageUrl}
            handleReferenceImageUpload={handleReferenceImageUpload}
            clearReferenceImage={clearReferenceImage}
          />
        </div>

        <Button
          onClick={validateAndGenerate}
          disabled={isGenerating}
          className="w-full bg-primary hover:bg-primary/90 text-white shadow-soft"
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
          <div className="bg-white rounded-lg shadow-soft p-5 border animate-fade-in">
            <PromptOutput generatedPrompt={generatedPrompt} />
          </div>
        )}
      </div>
    </div>
  );
};

export default PromptGenerationTab;
