import React from "react";
import { ImagePresets } from "@/lib/ImagePresets";
import KeywordSection from "./KeywordSection";
import ImageSettings from "./ImageSettings";

const SidebarSettings: React.FC = () => {
  const {
    keyword,
    setKeyword,
    keywords,
    handleAddKeyword,
    handleRemoveKeyword,
    handleKeywordImageUpload,
    styleStrength,
    setStyleStrength,
    resolution,
    handleResolutionChange,
    batchSize,
    setBatchSize,
    isLoadingKeywords,
  } = ImagePresets();

  return (
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
        styleStrength={styleStrength}
        setStyleStrength={setStyleStrength}
        resolution={resolution}
        handleResolutionChange={handleResolutionChange}
        batchSize={batchSize}
        setBatchSize={setBatchSize}
      />
    </div>
  );
};

export default SidebarSettings;
