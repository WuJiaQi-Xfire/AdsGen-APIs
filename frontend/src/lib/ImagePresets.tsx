import { useState } from "react";
import { showToast } from "@/lib/ShowToast";
import { ApiService } from "@/lib/api";

export const ImagePresets = () => {
  const [keyword, setKeyword] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
  const [styleStrength, setStyleStrength] = useState(80);
  const [resolution, setResolution] = useState({ width: 1024, height: 1024 });
  const [batchSize, setBatchSize] = useState(1);
  const [isLoadingKeywords, setIsLoadingKeywords] = useState(false);

  const handleAddKeyword = () => {
    if (keyword.trim()) {
      const newKeywords = keyword
        .split(",")
        .map((k) => k.trim())
        .filter((k) => k !== "" && !keywords.includes(k));

      if (newKeywords.length > 0) {
        setKeywords([...keywords, ...newKeywords]);
        setKeyword("");
      }
    }
  };

  const handleRemoveKeyword = (keywordToRemove: string) => {
    setKeywords(keywords.filter((k) => k !== keywordToRemove));
  };

  const handleKeywordImageUpload = async (file?: File, imageUrl?: string) => {
    try {
      setIsLoadingKeywords(true);
      const response = await ApiService.extractKeywords(file, imageUrl);
      const extractedKeywords = response.keywords || [];
      if (extractedKeywords.length > 0) {
        const newKeywords = extractedKeywords.filter(
          (k: string) => !keywords.includes(k)
        );

        if (newKeywords.length > 0) {
          setKeywords([...keywords, ...newKeywords]);
          showToast(
             `${newKeywords.length} new keyword${newKeywords.length !== 1 ? 's' : ''} extracted from your image.`
          );
        } else {
          showToast("All extracted keywords are already in your list.");
        }
      } else {
        showToast("No keywords could be extracted from the image.");
      }
    } catch (error) {
      console.error("Error in handleKeywordImageUpload:", error);
    } finally {
      setIsLoadingKeywords(false);
    }
  };

  const handleResolutionChange = (
    dimension: "width" | "height",
    value: string
  ) => {
    const numValue = parseInt(value, 10) || 0;
    setResolution((prev) => ({
      ...prev,
      [dimension]: numValue,
    }));
  };

  return {
    keyword,
    setKeyword,
    keywords,
    setKeywords,
    styleStrength,
    setStyleStrength,
    isLoadingKeywords,
    resolution,
    setResolution,
    batchSize,
    setBatchSize,
    handleAddKeyword,
    handleRemoveKeyword,
    handleKeywordImageUpload,
    handleResolutionChange,
  };
};
