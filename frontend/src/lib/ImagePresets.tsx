import { useState } from "react";
import { showToast } from "@/lib/ShowToast";

export const ImagePresets = () => {
  const [keyword, setKeyword] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
  const [styleStrength, setStyleStrength] = useState(80);
  const [resolution, setResolution] = useState({ width: 1024, height: 1024 });
  const [batchSize, setBatchSize] = useState(1);

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

  const handleKeywordImageUpload = () => {
    // TODO, encode image in base64 and pass to GPT and get the generated keywords
    // FOr now: Simulate keyword extraction from image
    setTimeout(() => {
      const extractedKeywords = ["chaos", "war", "fighting"];
      setKeywords([...keywords, ...extractedKeywords]);
      showToast("Keywords generated from your reference image.");
    }, 1500);
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
