import { useState } from "react";
import { ArrowRight, RefreshCw } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { ImageGeneration } from "@/lib/ImageGeneration";
import PromptSection from "./Image/PromptSection";
import StyleSection from "./Image/StyleSection.tsx";
import KeywordSection from "./Image/KeywordSection";
import ImageSettings from "./Image/ImageSettings";
import { showToast } from "@/lib/ShowToast";
import { ImagePresets } from "@/lib/ImagePresets";
import { ScrollArea } from "@/components/UI/ScrollArea.tsx";
import { ApiService, PromptFile } from "@/lib/api";

const ImageGenerationTab: React.FC = () => {
  const [hasGenerated, setHasGenerated] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImages, setGeneratedImages] = useState<string[]>([]);

  const {
    promptFiles,
    hasPrompt,
    handlePromptUpload,
    promptFileInputRef,
    handlePromptFileUpload,
    styleType,
    setStyleType,
    selectedStyles,
    searchQuery,
    setSearchQuery,
    selectMode,
    setSelectMode,
    toggleStyleSelection,
    togglePromptSelection,
    selectAllStyles,
    clearStyleSelection,
    selectRandomStyle,
    filteredStyles,
    fileInputRef,
  } = ImageGeneration();

  const {
    keyword,
    setKeyword,
    keywords,
    handleAddKeyword,
    handleRemoveKeyword,
    handleKeywordImageUpload,
    resolution,
    handleResolutionChange,
    batchSize,
    setBatchSize,
    isLoadingKeywords,
  } = ImagePresets();

  const handleGenerate = async () => {
    if (promptFiles.length === 0) {
      showToast("Please upload at least one prompt.");
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

    if (keywords.length === 0) {
      showToast("Please enter at least one keyword");
      return;
    }

    setIsGenerating(true);
    try {
      const response = await ApiService.generateImage(
        selectedPrompts,
        selectedStyles,
        resolution.width,
        resolution.height,
        batchSize,
        keywords
      );
      //console.log("Image: ", response.images);
      const newImages = response.images;
      setGeneratedImages((prev) => {
        const combined = [...newImages, ...prev];
        if (combined.length > 10) {
          return combined.slice(0, 10); // Display only up to 10
        }
        return combined;
      });
      setHasGenerated(true);
      showToast("Your image has been generated successfully.");
      // Testing backend output
      console.log("Generated images:", response);
    } catch (error: any) {
      console.error("Error in handleGenerate image:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleRegenerate = () => {
    if (hasGenerated) {
      window.location.reload();
    } else {
      handleGenerate();
    }
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
              onClick={handleRegenerate}
              disabled={isGenerating}
              className="w-full bg-primary hover:bg-primary/90 text-white shadow-soft"
              size="lg"
            >
              {isGenerating ? (
                "Generating..."
              ) : hasGenerated ? (
                <>
                  Regenerate <RefreshCw className="ml-2 h-4 w-4" />
                </>
              ) : (
                <>
                  Generate Image <ArrowRight className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          </div>

          {generatedImages.length > 0 && (
            <div className="pt-6">
              <h3 className="text-lg font-medium mb-3">Generated Images</h3>
              <Button
                //onClick={}
                className="w-full bg-primary hover:bg-primary/90 text-white shadow-soft"
                size="lg"
              >
                Download Image
              </Button>
              <ScrollArea className="w-full">
                <div className="flex space-x-4 pb-4">
                  {generatedImages.map((image, index) => (
                    <div key={index} className="flex-shrink-0 w-48">
                      <div className="relative rounded-md overflow-hidden border shadow-sm">
                        <img
                          src={image}
                          alt={`Generated image ${index + 1}`}
                          className="w-full h-48 object-cover"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </div>
          )}
        </div>

        <div className="md:col-span-1">
          <div className="space-y-6 border rounded-lg p-5 shadow-soft bg-white">
            <KeywordSection
              keyword={keyword}
              setKeyword={setKeyword}
              keywords={keywords}
              handleAddKeyword={handleAddKeyword}
              handleRemoveKeyword={handleRemoveKeyword}
              isLoadingKeywords={isLoadingKeywords}
              handleKeywordImageUpload={handleKeywordImageUpload}
            />

            <ImageSettings
              resolution={resolution}
              handleResolutionChange={handleResolutionChange}
              batchSize={batchSize}
              setBatchSize={setBatchSize}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageGenerationTab;
