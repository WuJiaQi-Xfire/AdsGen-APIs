import { useState } from "react";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { ImageGeneration } from "@/lib/ImageGeneration";
import PromptSection from "./Image/PromptSection";
import StyleSection from "./Image/StyleSection.tsx";
import KeywordSection from "./Image/KeywordSection";
import ImageSettings from "./Image/ImageSettings";
import { showToast } from "@/lib/ShowToast";
import { ImagePresets } from "@/lib/ImagePresets";
import ImageGallery, { GeneratedImage } from "./Image/ImageGallery";
import { ApiService, PromptFile } from "@/lib/api";

const ImageGenerationTab: React.FC = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImages, setGeneratedImages] = useState<GeneratedImage[]>([]);

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
    toggleStyleSelection,
    togglePromptSelection,
    selectAllStyles,
    clearStyleSelection,
    selectRandomStyle,
    filteredStyles,
    fileInputRef,
    loraStyles,
    artStyles,
  } = ImageGeneration();

  const {
    keyword,
    setKeyword,
    keywords,
    handleAddKeyword,
    handleRemoveKeyword,
    handleKeywordImageUpload,
    styleStrength,
    setStyleStrength,
    aspectRatio,
    handleResolutionChange,
    batchSize,
    setBatchSize,
    isLoadingKeywords,
    addStyleSetting,
    removeStyleSetting,
    updateStyleSetting,
    getStyleSettings,
    getAllStyleSettings,
    activeStyleId,
    setActiveStyleId,
    styleSettings,
    stackLoRAs,
    setStackLoRAs,
  } = ImagePresets();

  const getActiveStyleName = () => {
    if (!activeStyleId) return undefined;

    const style = filteredStyles.find((s) => s.id === activeStyleId);
    return style?.name;
  };

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
      const styleTypeMap = new Map<string, "lora" | "art">();

      // Add all LoRA styles to the map
      loraStyles.forEach((style) => {
        styleTypeMap.set(style.id, "lora");
      });

      // Add all art styles to the map
      artStyles.forEach((style) => {
        styleTypeMap.set(style.id, "art");
      });

      const styleSettingsToSend = styleSettings
        .filter((setting) => selectedStyles.includes(setting.id))
        .map((setting) => {
          const styleType = setting.styleType || styleTypeMap.get(setting.id);

          if (!styleType) {
            console.warn(`No styleType found for style: ${setting.id}`);
          }

          return {
            id: setting.id,
            styleStrength: setting.styleStrength,
            batchSize: setting.batchSize,
            aspectRatio: setting.aspectRatio,
            styleType: styleType || "art",
          };
        });

      const missingStyles = selectedStyles.filter(
        (styleId) =>
          !styleSettingsToSend.some((setting) => setting.id === styleId)
      );

      for (const styleId of missingStyles) {
        // First try to find the style in the complete style list (both LoRA and art)
        const styleType = styleTypeMap.get(styleId);

        if (styleType) {
          styleSettingsToSend.push({
            id: styleId,
            styleStrength,
            batchSize,
            aspectRatio,
            styleType,
          });
        } else {
          console.warn(`No style found for ID: ${styleId}`);
        }
      }

      const response = await ApiService.generateImage(
        selectedPrompts,
        styleSettingsToSend,
        keywords,
        stackLoRAs
      );
      if (response.images && response.images.length > 0) {
        const images: GeneratedImage[] = response.images.map((img) => ({
          url: img.data,
          filename: img.filename,
          selected: false,
        }));

        setGeneratedImages(images);
        showToast("Images generated successfully!");
      } else {
        showToast("No images were generated. Please try again.");
      }
    } catch (error: any) {
      console.error("Error generating images:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSelectImage = (index: number) => {
    setGeneratedImages((prev) =>
      prev.map((img, i) =>
        i === index ? { ...img, selected: !img.selected } : img
      )
    );
  };

  const handleDownloadSelected = () => {
    const selectedImages = generatedImages.filter((img) => img.selected);

    if (selectedImages.length === 0) {
      showToast("Please select at least one image to download");
      return;
    }

    selectedImages.forEach((image, index) => {
      const link = document.createElement("a");
      link.href = image.url;
      link.download = `generated-image-${image.filename || index}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });

    showToast(
      `Downloaded ${selectedImages.length} image${
        selectedImages.length !== 1 ? "s" : ""
      }`
    );
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
              toggleStyleSelection={toggleStyleSelection}
              filteredStyles={filteredStyles}
              selectAllStyles={selectAllStyles}
              clearStyleSelection={clearStyleSelection}
              selectRandomStyle={selectRandomStyle}
              fileInputRef={fileInputRef}
              setActiveStyleId={setActiveStyleId}
              activeStyleId={activeStyleId}
              addStyleSetting={addStyleSetting}
              removeStyleSetting={removeStyleSetting}
              styleSettings={styleSettings}
              updateStyleSetting={updateStyleSetting}
              stackLoRAs={stackLoRAs}
              setStackLoRAs={setStackLoRAs}
            />
          </div>

          <div className="pt-4">
            <Button
              onClick={handleGenerate}
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

          {generatedImages.length > 0 && (
            <div className="pt-6 bg-white rounded-lg shadow-soft p-5 border">
              <ImageGallery
                images={generatedImages}
                onSelectImage={handleSelectImage}
                onDownloadSelected={handleDownloadSelected}
                isLoading={isGenerating}
              />
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
              handleKeywordImageUpload={handleKeywordImageUpload}
              isLoadingKeywords={isLoadingKeywords}
            />

            <ImageSettings
              aspectRatio={aspectRatio}
              handleAspectRatioChange={handleResolutionChange}
              styleStrength={styleStrength}
              setStyleStrength={setStyleStrength}
              batchSize={batchSize}
              setBatchSize={setBatchSize}
              activeStyleId={activeStyleId}
              activeStyleName={getActiveStyleName()}
              selectedStyles={selectedStyles}
              styleSettings={styleSettings}
              updateStyleSetting={updateStyleSetting}
              setActiveStyleId={setActiveStyleId}
              filteredStyles={filteredStyles}
              stackLoRAs={stackLoRAs}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageGenerationTab;
