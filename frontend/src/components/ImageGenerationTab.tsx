import React from "react";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { ImageGeneration } from "@/lib/ImageGeneration";
import PromptSection from "./Image/PromptSection";
import StyleSection from "./Image/StyleSection.tsx";
import SideBarSettings from "./Image/SideBarSettings.tsx";
import { showToast } from "@/lib/ShowToast";

const ImageGenerationTab: React.FC = () => {
  const {
    promptFiles,
    hasPrompt,
    isGenerating,
    handlePromptUpload,
    promptFileInputRef,
    promptFileName,
    handlePromptFileUpload,
    styleType,
    setStyleType,
    selectedStyles,
    searchQuery,
    setSearchQuery,
    selectMode,
    setSelectMode,
    handleGenerate,
    toggleStyleSelection,
    togglePromptSelection,
    selectAllStyles,
    clearStyleSelection,
    selectRandomStyle,
    filteredStyles,
    fileInputRef,
  } = ImageGeneration();

  const validateAndGenerate = () => {
    if (!hasPrompt || promptFiles.length === 0) {
      showToast("Please upload at least one prompt file first.");
      return;
    }

    const selectedPrompts = promptFiles.filter((file) => file.selected);
    if (selectedPrompts.length === 0) {
      showToast("Please select at least one prompt.");
      return;
    }
    
    if (selectedStyles.length === 0) {
      showToast("Please select at least one style.");
      return;
    }

    handleGenerate();
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-6 animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-1">
          Image Generation
        </h1>
        <p className="text-muted-foreground">Generate custom images using AI</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <div className="bg-white rounded-lg shadow-soft p-5 border">
            <PromptSection
              hasPrompt={hasPrompt}
              promptFiles={promptFiles}
              togglePromptSelection={togglePromptSelection}
              handlePromptUpload={handlePromptUpload}
              promptFileInputRef={promptFileInputRef}
              handlePromptFileUpload={handlePromptFileUpload}
            />
          </div>
          <div className="bg-white rounded-lg shadow-soft p-5 border">
            <StyleSection
              styleType={styleType}
              setStyleType={setStyleType}
              selectedStyles={selectedStyles}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              selectMode={selectMode}
              setSelectMode={setSelectMode}
              toggleStyleSelection={toggleStyleSelection}
              filteredStyles={filteredStyles}
              selectAllStyles={selectAllStyles}
              clearStyleSelection={clearStyleSelection}
              selectRandomStyle={selectRandomStyle}
              fileInputRef={fileInputRef}
            />
          </div>

          <div className="pt-4">
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
                  Generate Image <ArrowRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </div>

        <div className="md:col-span-1">
          <SideBarSettings />
        </div>
      </div>
    </div>
  );
};

export default ImageGenerationTab;
