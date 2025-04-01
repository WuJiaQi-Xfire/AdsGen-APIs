import { useState, useEffect } from "react";
import { showToast } from "@/lib/ShowToast";
import { ApiService } from "@/lib/api";

// Interface for individual style settings
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
  
  // Default settings for new styles
  const [defaultSettings, setDefaultSettings] = useState({
    styleStrength: 1,
    batchSize: 1,
    width: 1024,
    height: 1024
  });
  
  // Settings for each selected style
  const [styleSettings, setStyleSettings] = useState<StyleSettings[]>([]);
  
  // Currently selected style for settings panel
  const [activeStyleId, setActiveStyleId] = useState<string | null>(null);
  
  const [isLoadingKeywords, setIsLoadingKeywords] = useState(false);

  // For backward compatibility
  const styleStrength = defaultSettings.styleStrength;
  const setStyleStrength = (value: number) => {
    setDefaultSettings(prev => ({ ...prev, styleStrength: value }));
    
    // If a style is active, also update its settings
    if (activeStyleId) {
      updateStyleSetting(activeStyleId, "styleStrength", value);
    }
  };
  
  const resolution = { width: defaultSettings.width, height: defaultSettings.height };
  const batchSize = defaultSettings.batchSize;
  
  const setBatchSize = (value: number) => {
    setDefaultSettings(prev => ({ ...prev, batchSize: value }));
    
    // If a style is active, also update its settings
    if (activeStyleId) {
      updateStyleSetting(activeStyleId, "batchSize", value);
    }
  };

  // Add a new style to track settings for
  const addStyleSetting = (id: string, name: string) => {
    // Check if style already exists
    if (!styleSettings.some(s => s.id === id)) {
      setStyleSettings(prev => [
        ...prev,
        {
          id,
          name,
          styleStrength: defaultSettings.styleStrength,
          batchSize: defaultSettings.batchSize,
          width: defaultSettings.width,
          height: defaultSettings.height
        }
      ]);
    }
    
    // Set as active style
    setActiveStyleId(id);
  };

  // Remove a style's settings
  const removeStyleSetting = (id: string) => {
    setStyleSettings(prev => prev.filter(s => s.id !== id));
    
    // If the active style is removed, set active to null
    if (activeStyleId === id) {
      setActiveStyleId(null);
    }
  };

  // Update a specific setting for a style
  const updateStyleSetting = (id: string, setting: keyof Omit<StyleSettings, 'id' | 'name'>, value: number) => {
    setStyleSettings(prev => 
      prev.map(s => 
        s.id === id 
          ? { ...s, [setting]: value } 
          : s
      )
    );
  };

  // Get settings for a specific style
  const getStyleSettings = (id: string): StyleSettings | undefined => {
    return styleSettings.find(s => s.id === id);
  };

  // Get all style settings
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
    setDefaultSettings(prev => ({
      ...prev,
      [dimension]: numValue
    }));
    
    // If a style is active, also update its settings
    if (activeStyleId) {
      updateStyleSetting(activeStyleId, dimension as keyof Omit<StyleSettings, 'id' | 'name'>, numValue);
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
    
    // New style-specific settings functions
    addStyleSetting,
    removeStyleSetting,
    updateStyleSetting,
    getStyleSettings,
    getAllStyleSettings,
    activeStyleId,
    setActiveStyleId,
    styleSettings
  };
};
