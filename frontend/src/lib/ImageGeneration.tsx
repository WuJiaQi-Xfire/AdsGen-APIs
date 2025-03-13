import { useState, useRef } from "react";
import { showToast } from "@/lib/ShowToast";
import { getStyles } from "@/lib/ArtStyleList";

export const useImageGeneration = () => {
  const [prompt, setPrompt] = useState("");
  const [hasPrompt, setHasPrompt] = useState(false);
  const [promptText, setPromptText] = useState("");
  const [keyword, setKeyword] = useState("");
  const [keywords, setKeywords] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedStyles, setSelectedStyles] = useState<string[]>([]);
  const [styleType, setStyleType] = useState<"lora" | "art">("lora");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectMode, setSelectMode] = useState<"single" | "multiple">("single");
  const [styleStrength, setStyleStrength] = useState(80);
  const [resolution, setResolution] = useState({ width: 1024, height: 1024 });
  const [batchSize, setBatchSize] = useState(1);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const promptFileInputRef = useRef<HTMLInputElement>(null);
  const [promptFileName, setPromptFileName] = useState("");
  const [hasReferenceImage, setHasReferenceImage] = useState(false);
  const [referenceImageFileName, setReferenceImageFileName] = useState("");
  const [referenceImageUrl, setReferenceImageUrl] = useState("");
  const { filteredStyles } = getStyles(styleType, searchQuery);

  const handlePromptFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length === 1) {
      const file = e.target.files[0];
      setPromptFileName(file.name);

      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setPromptText(event.target.result as string);
          setHasPrompt(true);

          showToast("${file.name} has been loaded successfully.");
        }
      };

      reader.onerror = () => {
        showToast("There was an error reading the file content.");
      };

      reader.readAsText(file);
    }
  };

  const handlePromptUpload = () => {
    if (promptFileInputRef.current) {
      promptFileInputRef.current.click();
    }
  };

  const handleReferenceImageUpload = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (e.target.files && e.target.files.length === 1) {
      const file = e.target.files[0];
      setReferenceImageFileName(file.name);
      setHasReferenceImage(true);
      setReferenceImageUrl("");

      showToast("${file.name} has been selected as reference.");
    }
  };

  const clearReferenceImage = () => {
    setHasReferenceImage(false);
    setReferenceImageFileName("");
    setReferenceImageUrl("");
  };

  const handleGenerate = () => {
    setIsGenerating(true);
    // Simulate generation
    setTimeout(() => {
      setIsGenerating(false);
      showToast("Your image has been generated successfully.");
    }, 1500);
  };

  const toggleStyleSelection = (styleId: string) => {
    if (selectMode === "single") {
      setSelectedStyles([styleId]);
    } else {
      if (selectedStyles.includes(styleId)) {
        setSelectedStyles(selectedStyles.filter((id) => id !== styleId));
      } else {
        setSelectedStyles([...selectedStyles, styleId]);
      }
    }
  };

  const selectAllStyles = () => {
    setSelectedStyles(filteredStyles.map((style) => style.id));
  };

  const clearStyleSelection = () => {
    setSelectedStyles([]);
  };

  const selectRandomStyle = () => {
    const randomIndex = Math.floor(Math.random() * filteredStyles.length);
    setSelectedStyles([filteredStyles[randomIndex].id]);
  };

  return {
    prompt,
    setPrompt,
    hasPrompt,
    setHasPrompt,
    promptText,
    setPromptText,
    keyword,
    setKeyword,
    keywords,
    setKeywords,
    isGenerating,
    selectedStyles,
    styleType,
    setStyleType,
    searchQuery,
    setSearchQuery,
    selectMode,
    setSelectMode,
    styleStrength,
    setStyleStrength,
    resolution,
    setResolution,
    batchSize,
    setBatchSize,
    fileInputRef,
    promptFileInputRef,
    promptFileName,
    handlePromptUpload,
    handlePromptFileUpload,
    toggleStyleSelection,
    selectAllStyles,
    clearStyleSelection,
    selectRandomStyle,
    filteredStyles,
    hasReferenceImage,
    referenceImageFileName,
    referenceImageUrl,
    setReferenceImageUrl,
    handleGenerate,
    handleReferenceImageUpload,
    clearReferenceImage,
  };
};
