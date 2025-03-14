import React from "react";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { ImageGeneration } from "@/lib/ImageGeneration";
import PromptSection from "./Image/PromptSection";
import StyleSection from "./Image/StyleSection.tsx";
import SideBar from "./Image/SideBar";

const ImageGenerationTab: React.FC = () => {
  const {
    promptText,
    hasPrompt,
    isGenerating,
    handlePromptUpload,
    promptFileInputRef,
    promptFileName,
    handlePromptFileUpload,
    setPromptText,
    setHasPrompt,
    styleType,
    setStyleType,
    selectedStyles,
    searchQuery,
    setSearchQuery,
    selectMode,
    setSelectMode,
    handleGenerate,
    toggleStyleSelection,
    selectAllStyles,
    clearStyleSelection,
    selectRandomStyle,
    filteredStyles,
    fileInputRef,
  } = ImageGeneration();

  return (
    <div className="w-full max-w-4xl mx-auto p-6 animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-1">
          Image Generation
        </h1>
        <p className="text-muted-foreground">Generate custom images using AI</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        <div className="md:col-span-8 space-y-6">
          <PromptSection
            hasPrompt={hasPrompt}
            promptText={promptText}
            promptFileName={promptFileName}
            setPromptText={setPromptText}
            setHasPrompt={setHasPrompt}
            handlePromptUpload={handlePromptUpload}
            promptFileInputRef={promptFileInputRef}
            handlePromptFileUpload={handlePromptFileUpload}
          />

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

          <div className="pt-4">
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
                  Generate Image <ArrowRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </div>

        <div className="md:col-span-4">
          <SideBar />
        </div>
      </div>
    </div>
  );
};

export default ImageGenerationTab;
