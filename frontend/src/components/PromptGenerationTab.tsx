import React from "react";
import { Button } from "@/components/UI/PrimaryButton";
import { ArrowRight } from "lucide-react";
import PromptInput from "./Prompt/PromptInput";
import ReferenceImage from "./Prompt/ReferenceImage";
import PromptOutput from "./Prompt/PromptOutput";
import { PromptGeneration } from "@/lib/PromptGeneration";

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
        <PromptInput
          description={description}
          setDescription={setDescription}
        />

        <ReferenceImage
          hasReferenceImage={hasReferenceImage}
          fileName={fileName}
          imageUrl={imageUrl}
          setImageUrl={setImageUrl}
          handleReferenceImageUpload={handleReferenceImageUpload}
          clearReferenceImage={clearReferenceImage}
        />

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

        {generatedPrompt && <PromptOutput generatedPrompt={generatedPrompt} />}
      </div>
    </div>
  );
};

export default PromptGenerationTab;
