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

  const handleKeywordImageUpload = async (file?: File, imageUrl?: string) => {
    try {
      const formData = new FormData();

      if (file) {
        formData.append("image", file);
      } else if (imageUrl) {
        formData.append("image_url", imageUrl);
      } else {
        throw new Error("No image provided");
      }

      const response = await fetch(
        "http://127.0.0.1:8000/api/extract-keywords/",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to extract keywords");
      }

      const data = await response.json();
      const extractedKeywords = data.keywords || [];

      if (extractedKeywords.length > 0) {
        setKeywords([...keywords, ...extractedKeywords]);
        showToast(
          "${extractedKeywords.length} keywords extracted from your image."
        );
      } else {
        showToast("No keywords could be extracted from the image.");
      }
    } catch (error) {
      console.error("Error extracting keywords:", error);
      showToast("There was an error extracting keywords. Please try again.");
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
