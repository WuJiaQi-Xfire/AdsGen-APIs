import { useState } from "react";
import { showToast } from "@/lib/ShowToast";
import { ApiService } from "@/lib/api";

export interface StyleSettings {
  id: string;
  name: string;
  styleStrength: number;
  batchSize: number;
  width: number;
  height: number;
}

export const ImagePresets = () => {
  const [keyword, setKeyword] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);

  const [defaultSettings, setDefaultSettings] = useState({
    styleStrength: 1,
    batchSize: 1,
    width: 1024,
    height: 1024,
  });

  const [styleSettings, setStyleSettings] = useState<StyleSettings[]>([]);
  const [activeStyleId, setActiveStyleId] = useState<string | null>(null);
  const [isLoadingKeywords, setIsLoadingKeywords] = useState(false);

  const styleStrength = defaultSettings.styleStrength;
  const setStyleStrength = (value: number) => {
    setDefaultSettings((prev) => ({ ...prev, styleStrength: value }));

    if (activeStyleId) {
      updateStyleSetting(activeStyleId, "styleStrength", value);
    }
  };

  const resolution = {
    width: defaultSettings.width,
    height: defaultSettings.height,
  };
  const batchSize = defaultSettings.batchSize;

  const setBatchSize = (value: number) => {
    setDefaultSettings((prev) => ({ ...prev, batchSize: value }));

    if (activeStyleId) {
      updateStyleSetting(activeStyleId, "batchSize", value);
    }
  };

  const addStyleSetting = (id: string, name: string) => {
    if (!styleSettings.some((s) => s.id === id)) {
      setStyleSettings((prev) => [
        ...prev,
        {
          id,
          name,
          styleStrength: defaultSettings.styleStrength,
          batchSize: defaultSettings.batchSize,
          width: defaultSettings.width,
          height: defaultSettings.height,
        },
      ]);
    }

    setActiveStyleId(id);
  };

  const removeStyleSetting = (id: string) => {
    setStyleSettings((prev) => prev.filter((s) => s.id !== id));

    if (activeStyleId === id) {
      setActiveStyleId(null);
    }
  };

  const updateStyleSetting = (
    id: string,
    setting: keyof Omit<StyleSettings, "id" | "name">,
    value: number
  ) => {
    setStyleSettings((prev) =>
      prev.map((s) => (s.id === id ? { ...s, [setting]: value } : s))
    );
  };

  const getStyleSettings = (id: string): StyleSettings | undefined => {
    return styleSettings.find((s) => s.id === id);
  };

  const getAllStyleSettings = (): StyleSettings[] => {
    return styleSettings;
  };

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
            `${newKeywords.length} new keyword${
              newKeywords.length !== 1 ? "s" : ""
            } extracted from your image.`
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
    setDefaultSettings((prev) => ({
      ...prev,
      [dimension]: numValue,
    }));

    if (activeStyleId) {
      updateStyleSetting(
        activeStyleId,
        dimension as keyof Omit<StyleSettings, "id" | "name">,
        numValue
      );
    }
  };

  return {
    keyword,
    setKeyword,
    keywords,
    setKeywords,
    isLoadingKeywords,
    styleStrength,
    setStyleStrength,
    resolution,
    batchSize,
    setBatchSize,
    handleAddKeyword,
    handleRemoveKeyword,
    handleKeywordImageUpload,
    handleResolutionChange,
    addStyleSetting,
    removeStyleSetting,
    updateStyleSetting,
    getStyleSettings,
    getAllStyleSettings,
    activeStyleId,
    setActiveStyleId,
    styleSettings,
  };
};
