import { useState, useEffect } from "react";
import { showToast } from "@/lib/ShowToast";
import { ApiService, KeywordExtractionResponse } from "@/lib/api";

export interface StyleSettings {
  id: string;
  name: string;
  styleStrength: number;
  batchSize: number;
  //aspectRatio: "1:1" | "16:9" | "9:16";
  styleType: "lora" | "art";
}

export const ImagePresets = () => {
  const [keyword, setKeyword] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
  const [stackLoRAs, setStackLoRAs] = useState(false);

  const [defaultSettings, setDefaultSettings] = useState(() => {
    const savedSettings = localStorage.getItem("defaultStyleSettings");
    if (savedSettings) {
      try {
        return JSON.parse(savedSettings);
      } catch (e) {
        console.error("Error parsing saved settings:", e);
      }
    }
    return {
      styleStrength: 1,
      batchSize: 1,
      //aspectRatio: "1:1",
    };
  });

  const [styleSettings, setStyleSettings] = useState<StyleSettings[]>(() => {
    const savedStyleSettings = localStorage.getItem("styleSettings");
    if (savedStyleSettings) {
      try {
        return JSON.parse(savedStyleSettings);
      } catch (e) {
        console.error("Error parsing saved style settings:", e);
      }
    }
    return [];
  });

  const [activeStyleId, setActiveStyleId] = useState<string | null>(null);
  const [isLoadingKeywords, setIsLoadingKeywords] = useState(false);

  useEffect(() => {
    localStorage.setItem(
      "defaultStyleSettings",
      JSON.stringify(defaultSettings)
    );
  }, [defaultSettings]);

  useEffect(() => {
    localStorage.setItem("styleSettings", JSON.stringify(styleSettings));
  }, [styleSettings]);

  const handleAddKeyword = (newKeyword: string) => {
    if (!newKeyword.trim()) return;

    if (keywords.includes(newKeyword.trim())) {
      showToast("Keyword already exists");
      return;
    }

    setKeywords([...keywords, newKeyword.trim()]);
    setKeyword("");
  };

  const handleRemoveKeyword = (keywordToRemove: string) => {
    setKeywords(keywords.filter((k) => k !== keywordToRemove));
  };

  const addStyleSetting = (
    id: string,
    name: string,
    styleType: "lora" | "art"
  ) => {
    const existingSetting = styleSettings.find((s) => s.id === id);

    if (existingSetting) {
      return;
    }

    const newStyleSetting: StyleSettings = {
      id,
      name,
      styleStrength: defaultSettings.styleStrength,
      batchSize: defaultSettings.batchSize,
      //aspectRatio: defaultSettings.aspectRatio,
      styleType,
    };

    setStyleSettings([...styleSettings, newStyleSetting]);
    setActiveStyleId(id);
  };

  const removeStyleSetting = (id: string) => {
    setStyleSettings(styleSettings.filter((s) => s.id !== id));

    if (activeStyleId === id) {
      setActiveStyleId(null);
    }
  };

  const getStyleSettings = (id: string | null): StyleSettings | null => {
    if (!id) return null;

    const setting = styleSettings.find((s) => s.id === id);
    return setting || null;
  };

  const getAllStyleSettings = (): StyleSettings[] => {
    return styleSettings;
  };

  const updateStyleSetting = (
    id: string,
    setting: keyof Omit<StyleSettings, "id" | "name">,
    value: number | "1:1" | "16:9" | "9:16" | "lora" | "art"
  ) => {
    setStyleSettings(
      styleSettings.map((s) => {
        if (s.id === id) {
          return { ...s, [setting]: value };
        }
        return s;
      })
    );
  };

  const handleKeywordImageUpload = async (file?: File, imageUrl?: string) => {
    try {
      setIsLoadingKeywords(true);
      let response: KeywordExtractionResponse;
      response = await ApiService.extractKeywords(
        file || null,
        imageUrl || null
      );

      if (response.keywords && response.keywords.length > 0) {
        setKeywords(response.keywords);
        showToast("Keywords extracted successfully");
      } else {
        showToast("No keywords found in the image");
      }
    } catch (error) {
      console.error("Error extracting keywords:", error);
      showToast("Failed to extract keywords");
    } finally {
      setIsLoadingKeywords(false);
    }
  };
  /*
  const handleResolutionChange = (aspectRatio: "1:1" | "16:9" | "9:16") => {
    setDefaultSettings((prev) => ({
      ...prev,
      aspectRatio,
    }));

    if (activeStyleId) {
      updateStyleSetting(activeStyleId, "aspectRatio", aspectRatio);
    }
  };
  */
  const setStyleStrength = (value: number) => {
    setDefaultSettings((prev) => ({
      ...prev,
      styleStrength: value,
    }));

    if (activeStyleId) {
      updateStyleSetting(activeStyleId, "styleStrength", value);
    }
  };

  const setBatchSize = (value: number) => {
    setDefaultSettings((prev) => ({
      ...prev,
      batchSize: value,
    }));

    if (activeStyleId) {
      updateStyleSetting(activeStyleId, "batchSize", value);
    }
  };

  const styleStrength = activeStyleId
    ? getStyleSettings(activeStyleId)?.styleStrength ||
      defaultSettings.styleStrength
    : defaultSettings.styleStrength;

  const batchSize = activeStyleId
    ? getStyleSettings(activeStyleId)?.batchSize || defaultSettings.batchSize
    : defaultSettings.batchSize;

  /*
    const aspectRatio = activeStyleId
    ? getStyleSettings(activeStyleId)?.aspectRatio ||
      defaultSettings.aspectRatio
    : defaultSettings.aspectRatio;
  */
  return {
    keyword,
    setKeyword,
    keywords,
    handleAddKeyword,
    handleRemoveKeyword,
    handleKeywordImageUpload,
    styleStrength: defaultSettings.styleStrength,
    setStyleStrength: (value: number) =>
      setDefaultSettings({ ...defaultSettings, styleStrength: value }),
    //aspectRatio,
    //handleResolutionChange,
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
  };
};

export default ImagePresets;
